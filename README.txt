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

