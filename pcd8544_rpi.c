/*
=================================================================================
 Name        : pcd8544_rpi.c
 Version     : 3.0

##############################
 modify code by rei1984 @ Raspifans.com 
 add IP address. 20160316
 add CPU thermal degree 20160521
##############################

 Copyright (C) 2012 by Andre Wussow, 2012, desk@binerry.de

 Description :
     A simple PCD8544 LCD  for Raspberry Pi for displaying some system informations.
	 Makes use of WiringPI-library of Gordon Henderson (https://projects.drogon.net/raspberry-pi/wiringpi/)

	 Recommended connection (http://www.raspberrypi.org/archives/384):
	 LCD pins      Raspberry Pi
	 LCD1 - GND    P06  - GND
	 LCD2 - VCC    P01 - 3.3V
	 LCD3 - CLK    P11 - GPIO0
	 LCD4 - Din    P12 - GPIO1
	 LCD5 - D/C    P13 - GPIO2
	 LCD6 - CS     P15 - GPIO3
	 LCD7 - RST    P16 - GPIO4
	 LCD8 - LED    P01 - 3.3V 

================================================================================
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
================================================================================
 */
#include <wiringPi.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/sysinfo.h>
#include "PCD8544.h"

//ip address header files
#include <sys/types.h>
#include <ifaddrs.h>
#include <netinet/in.h>
#include <string.h>
#include <arpa/inet.h>




// pin setup
int _din = 1;
int _sclk = 0;
int _dc = 2;
int _rst = 4;
int _cs = 3;
  
// lcd contrast 
//may be need modify to fit your screen!  normal: 30- 90 ,default is:45 !!!maybe modify this value!
int contrast = 45;  
  
int main (void)
{
	struct ifaddrs * ifAddrStruct=NULL;
	void * tmpAddrPtr=NULL;

	getifaddrs(&ifAddrStruct);


  // print infos
  printf("Raspberry Pi PCD8544 sysinfo display\n");
  printf("========================================\n");
  
  // check wiringPi setup
  if (wiringPiSetup() == -1)
  {
	printf("wiringPi-Error\n");
    exit(1);
  }
  
  // init and clear lcd
  LCDInit(_sclk, _din, _dc, _cs, _rst, contrast);
  LCDclear();
  
  // show logo
  LCDshowLogo();
  
  delay(2000);
  
  for (;;)
  {
	  // clear lcd
	  LCDclear();
	  
	  // get system usage / info
	  struct sysinfo sys_info;
	  if(sysinfo(&sys_info) != 0)
	  {
		printf("sysinfo-Error\n");
	  }
	  
	  // uptime
	  char uptimeInfo[15];
	  unsigned long uptime = sys_info.uptime / 60;
	  sprintf(uptimeInfo, "Uptime %ld min.", uptime);
	  
	  // cpu info
	  char cpuInfo[10]; 
	  unsigned long avgCpuLoad = sys_info.loads[0] / 1000;
	  sprintf(cpuInfo, "CPU %ld%%", avgCpuLoad);
	  
	  // ram info
	  char ramInfo[10]; 
	  unsigned long totalRam = sys_info.freeram / 1024 / 1024;
	  sprintf(ramInfo, "RAM %ld MB", totalRam);
	  
		// IP address
		char IPInfo[15];
		while (ifAddrStruct!=NULL)
		{
			if (ifAddrStruct->ifa_addr->sa_family==AF_INET) 
			{   // check it is IP4 is a valid IP4 Address

				tmpAddrPtr=&((struct sockaddr_in *)ifAddrStruct->ifa_addr)->sin_addr;
				char addressBuffer[INET_ADDRSTRLEN];
				inet_ntop(AF_INET, tmpAddrPtr, addressBuffer, INET_ADDRSTRLEN);

				if( strcmp(ifAddrStruct->ifa_name,"eth0")==0)
				{
					strcpy(IPInfo,addressBuffer);
					//sprintf(IPInfo, "IP:%s", addressBuffer);
					break;
					//printf("%s IP4 Address %s\n", ifAddrStruct->ifa_name, addressBuffer);
				}
			}
			ifAddrStruct=ifAddrStruct->ifa_next;
		}
		
		char CPUTemp[15];
		{
			int i;

			for(i=0;i<15;i++)
			{
				CPUTemp[i]=0;
			}
		}



#include <sys/stat.h>  
#include <fcntl.h>  

#define TEMP_PATH "/sys/class/thermal/thermal_zone0/temp"  
#define MAX_SIZE 32  

    int fd;  
	double temp = 0;  
	char buf[MAX_SIZE];  

    fd = open(TEMP_PATH, O_RDONLY);  
	if (fd < 0)
	{  
		printf("failed to open thermal_zone0/temp\n");   
	}  

    // 读取内容  
	if (read(fd, buf, MAX_SIZE) < 0) 
	{  
		printf("failed to read temp\n");  
	}  

    // 转换为浮点数打印  
	temp = atoi(buf) / 1000.0;  
	printf("temp: %.2f\n", temp);  
	


	sprintf(CPUTemp,"CPUTemp:%.2f",temp);

	// 关闭文件  
	close(fd);  

















//		int fd = open("/sys/class/thermal/thermal_zone0/temp","rt");
//		if(fp)
//		{
//			fgets(text,5,fp);

//			printf("%s",text);



			//int temp = atoi(text);
			//sprintf(CPUTemp,"CPU Temp:%2d",temp/1000);
//			fclose(fp);		
//		}
//printf("88888888\n");
//printf("%s",CPUTemp);


	  // build screen
	  //LCDdrawstring(0, 0, "Raspberry Pi:");

	  LCDdrawstring(0, 1, "Raspberry Pi 0");
	  LCDdrawline(0, 10, 83, 10, BLACK);
	  LCDdrawstring(0, 12, uptimeInfo);
	  LCDdrawstring(0, 21, cpuInfo);
	  LCDdrawstring(0, 30, ramInfo);
	  //LCDdrawstring(0, 39, IPInfo);  //ip
	  LCDdrawstring(0, 39, CPUTemp);

	  LCDdisplay();
	  
	  delay(1000);
  }
  
    //for (;;){
  //  printf("LED On\n");
  //  digitalWrite(pin, 1);
  //  delay(250);
  //  printf("LED Off\n");
  //  digitalWrite(pin, 0);
  //  delay(250);
  //}

  return 0;
}
