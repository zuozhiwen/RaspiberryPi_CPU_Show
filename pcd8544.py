import ctypes
import datetime
from datetime import datetime
import os
import re
import RPi.GPIO as GPIO
import time
<<<<<<< HEAD
import dateutil.parser
import pika
import json
import threading
=======
>>>>>>> aa38d0660d7966a1b3a40d6310ff1ab1705b78c9

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
LED = 7
ON = 0
OFF = 1

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(LED, GPIO.OUT)

lib = ctypes.cdll.LoadLibrary('./PCD8544.so')
lib.wiringPiSetup()
lib.LCDInit(_sclk, _din, _dc, _cs, _rst, contrast)
lib.LCDclear()

# show logo
lib.LCDshowLogo()
lib.delay(1000)

for i in range(0, 6):
    GPIO.output(LED, i % 2)
    time.sleep(0.2)

if datetime.now().time() > dateutil.parser.parse('18:30').time() or datetime.now().time() < dateutil.parser.parse('7:00').time():
    GPIO.output(LED, ON)
else:
    GPIO.output(LED, OFF)

def show_cpu_info():
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

        if uptime > 3:
            temperature = float(os.popen('cat /sys/class/thermal/thermal_zone0/temp').read()) / 1000
            CPUTemp = "CPUTemp:%.2f" % temperature 
            lib.LCDdrawstring(0, 39, CPUTemp.encode())
        else:
            IPInfo = re.findall(r"wlan0[\s\S]+inet\s(\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b)", os.popen("ifconfig").read())[0]
            lib.LCDdrawstring(0, 39, IPInfo.encode())  #ip

        lib.LCDdisplay()
        lib.delay(2000)

def callback(ch,method,properties,body):
    ins = json.loads(body.decode())
    if ins['Action'] == 1:
        if ins['ExtraParams']['Switch'] == 'ON':
            GPIO.output(LED, ON)
        else:
            GPIO.output(LED, OFF)

def start_listen():
    user_pwd = pika.PlainCredentials('root', 'live01rabbit')
    connection = pika.BlockingConnection(pika.ConnectionParameters('47.98.181.100',5672,credentials=user_pwd))
    chan = connection.channel()
    chan.queue_declare(queue='RaspiberryPiWH')
    chan.basic_consume(callback, queue='RaspiberryPiWH', no_ack=True)
    chan.start_consuming()

threading.Thread(target=show_cpu_info).start()

start_listen()