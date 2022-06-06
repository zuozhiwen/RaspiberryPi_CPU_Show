import ctypes
from datetime import datetime
import os
import re
import RPi.GPIO as GPIO
import time
import dateutil.parser
import pika
import json
import threading
import psutil
import math

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


def flash_screen(round):
    for i in range(round * 2):
        GPIO.output(LED, i % 2)
        time.sleep(0.2)


def display_on_screen(uptime, loads, mem_info):
    # title
    lib.LCDclear()
    lib.LCDdrawstring(0, 1, b"Raspberry Pi 3")
    lib.LCDdrawline(0, 10, 83, 10, BLACK)
    
    # line 1
    if(uptime < 1000):
        uptime_info = "Uptime %d min." % uptime
    else:
        uptime_info = "Uptime %.1f h" % (uptime / 60.)
    lib.LCDdrawstring(0, 12, uptime_info.encode())
    
    # line 2
    cpu_info = 'CPU %d%%' % loads
    lib.LCDdrawstring(0, 21, cpu_info.encode())
    
    # line 3
    used_mem = mem_info.used
    ram_info = 'RAM {0} MB {1}%'.format(int(math.ceil(used_mem / 1024 / 1024)), int(mem_info.percent))
    lib.LCDdrawstring(0, 30, ram_info.encode())
    
    # line 4
    show_round = int(datetime.now().timestamp() / 15 % 2)
    if show_round == 1:
        sensors_temp = psutil.sensors_temperatures()
        cpu_temp = "CPUTemp:%.2f" % sensors_temp['cpu_thermal'][0].current
        lib.LCDdrawstring(0, 39, cpu_temp.encode())
    else:
        net_info = psutil.net_if_addrs()
        ip_address = net_info['wlan0'][0].address
        lib.LCDdrawstring(0, 39, ip_address.encode()) 
    
    lib.LCDdisplay()
    

def show_cpu_info():
    while True:
        uptime = (datetime.now().timestamp() - psutil.boot_time()) / 60
        loads = psutil.cpu_percent(interval=1)
        mem_info = psutil.virtual_memory()
        display_on_screen(uptime, loads, mem_info)
        lib.delay(2000)


def consume_method(ch, method, properties, body):
    ins = json.loads(body.decode())
    if ins['action'] == 1:
        if ins['params']['led'] == 1:
            GPIO.output(LED, ON)
        else:
            GPIO.output(LED, OFF)


def start_listen():
    with open('rabbitmq_password.txt') as f:
        rabbit_info = f.read().split('|')
        host = rabbit_info[0]
        username = rabbit_info[1]
        password = rabbit_info[2]
    user_pwd = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host, 5672, credentials=user_pwd))
    chan = connection.channel()
    chan.queue_declare('pi_command')
    chan.basic_consume('pi_command', consume_method, True)
    chan.start_consuming()


# =============================================================================================================================

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

flash_screen(3)

if datetime.now().time() > dateutil.parser.parse('18:30').time() or datetime.now().time() < dateutil.parser.parse('7:00').time():
    GPIO.output(LED, ON)
else:
    GPIO.output(LED, OFF)

showcpu = threading.Thread(target=show_cpu_info)
showcpu.setDaemon(True)
showcpu.start()

start_listen()
