# Raspiberry Pi Screen CPU Show
ref:http://raspifans.com/bbs/forum.php?mod=viewthread&tid=123
好的东西不应该在小的论坛被雪藏。这个程序是用C语言编写，用来将树莓派各种信息（cpu使用率、内存使用量、cpu温度、启动时间、IP等）展示到一块小小的屏幕上面，同时可以高度定制化（已经移植到python3），自定义任何信息，这取决个人的创造力。
![cpu show](http://github.com/zuozhiwen/RaspiberryPi_CPU_Show/blob/master/ScreenShot/2.jpg)
---
## Origin ReadMe
1.先安装wiring pi.

ref:http://wiringpi.com/wiringpi-and-the-raspberry-pi-compute-board/

cd ~
git clone git://git.drogon.net/wiringPi
cd wiringPi
./build



2.编译源代码
cc -o pcd8544_rpi pcd8544_rpi.c PCD8544.c  -L/usr/local/lib -lwiringPi


3.运行

sudo ./pcd8544_rpi

