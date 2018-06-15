import ctypes
import datetime
import os
import re

# pin setup
_din = 1
_sclk = 0
_dc = 2
_rst = 4
_cs = 3

# lcd contrast
# may be need modify to fit your screen!  normal: 30- 90 ,default is:45 !!!maybe modify this value!
contrast = 45

BLACK = 1
WHITE = 0

lib = ctypes.cdll.LoadLibrary('./PCD8544.so')
lib.wiringPiSetup()
lib.LCDInit(_sclk, _din, _dc, _cs, _rst, contrast)
lib.LCDclear()

# show logo
lib.LCDshowLogo()
lib.delay(1000)

while True:
    lib.LCDclear()
    lib.LCDdrawstring(0, 1, b"Raspberry Pi 0")
    lib.LCDdrawline(0, 10, 83, 10, BLACK)

    uptime = float(os.popen('cat /proc/uptime').read().split(' ')[0]) // 60
    uptimeInfo = "Uptime %d min." % uptime
    lib.LCDdrawstring(0, 12, uptimeInfo.encode())

    loads = 100 - float(re.findall(r',\s([1-9]\d*.\d*|0.\d*[1-9]\d*)\sid,', os.popen('top -bn 1 -i -c').read())[0])
    cpuInfo = 'CPU %d%%' % loads
    lib.LCDdrawstring(0, 21, cpuInfo.encode())

    mem_info_str = os.popen('cat /proc/meminfo').read()
    total_mem = int(re.findall(r'MemTotal:\s+(\d+)\s+kB', mem_info_str)[0])
    free_mem = int(re.findall(r'MemFree:\s+(\d+)\s+kB', mem_info_str)[0])
    ramInfo = 'RAM {0} MB {1}%'.format(int(free_mem / 1024), int((1 - free_mem / total_mem) * 100))
    lib.LCDdrawstring(0, 30, ramInfo.encode())

    if uptime >= 2:
        temperature = float(os.popen('cat /sys/class/thermal/thermal_zone0/temp').read()) / 1000
        CPUTemp = "CPUTemp:%.2f" % temperature 
        lib.LCDdrawstring(0, 39, CPUTemp.encode())
    else:
        IPInfo = re.findall(r"wlan0[\s\S]+inet\s(\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b)", os.popen("ifconfig").read())[0]
        lib.LCDdrawstring(0, 39, IPInfo.encode())  #ip

    lib.LCDdisplay()
    lib.delay(1000)

