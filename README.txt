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

