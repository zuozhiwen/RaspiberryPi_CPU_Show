# Raspiberry Pi Screen CPU Show
ref:http://raspifans.com/bbs/forum.php?mod=viewthread&tid=123
�õĶ�����Ӧ����С����̳��ѩ�ء������������C���Ա�д����������ݮ�ɸ�����Ϣ��cpuʹ���ʡ��ڴ�ʹ������cpu�¶ȡ�����ʱ�䡢IP�ȣ�չʾ��һ��СС����Ļ���棬ͬʱ���Ը߶ȶ��ƻ����Ѿ���ֲ��python3�����Զ����κ���Ϣ����ȡ�����˵Ĵ�������
![cpu show](http://github.com/zuozhiwen/RaspiberryPi_CPU_Show/blob/master/ScreenShot/2.jpg)
---
## Origin ReadMe
1.�Ȱ�װwiring pi.

ref:http://wiringpi.com/wiringpi-and-the-raspberry-pi-compute-board/

cd ~
git clone git://git.drogon.net/wiringPi
cd wiringPi
./build



2.����Դ����
cc -o pcd8544_rpi pcd8544_rpi.c PCD8544.c  -L/usr/local/lib -lwiringPi


3.����

sudo ./pcd8544_rpi

