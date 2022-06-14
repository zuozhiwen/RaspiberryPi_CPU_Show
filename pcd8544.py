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

display_mode = 'pi'

def flash_screen(round):
    for i in range(round * 2):
        GPIO.output(LED, i % 2)
        time.sleep(0.2)

def human_readable_size(size):
    unit = ['B', 'KB', 'MB', 'GB']
    unit_index = int(math.log(size, 1024))
    val = size / math.pow(1024, unit_index)

    final_str = '{0:.1f}'.format(val)[0:4].rstrip('.') + unit[unit_index]
    return final_str

def display_on_screen(uptime, loads, mem_info, host_name :str = None):
    if not host_name:
        host_name = "Raspberry Pi 3"
    
    # title
    lib.LCDclear()
    lib.LCDdrawstring(0, 1, host_name.encode())
    lib.LCDdrawline(0, 10, 83, 10, BLACK)

    # line 1
    if(uptime < 1000):
        uptime_info = "Uptime %d min." % uptime
    else:
        uptime_info = "Uptime %.1f h" % (uptime / 60.)
    lib.LCDdrawstring(0, 12, uptime_info.encode())

    # line 2
    cpu_info = 'CPU {0:.1f}%'.format(loads)
    lib.LCDdrawstring(0, 21, cpu_info.encode())

    # line 3
    used_mem = mem_info['used']
    ram_info = 'RAM {0} {1}%'.format(human_readable_size(used_mem), int(mem_info['percent']))
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
        if display_mode == 'pi':
            uptime = (datetime.now().timestamp() - psutil.boot_time()) / 60
            loads = psutil.cpu_percent(interval=1)
            raw_mem_info = psutil.virtual_memory()
            mem_info = {'used': raw_mem_info.used, 'percent': raw_mem_info.percent}
            display_on_screen(uptime, loads, mem_info)
        lib.delay(2000)


def consume_method(ch, method, properties, body):
    global display_mode
    msg = json.loads(body.decode())
    if msg['action'] == 1:
        if msg['params']['led'] == 1:
            GPIO.output(LED, ON)
        else:
            GPIO.output(LED, OFF)
    elif msg['action'] == 2:
        if display_mode != 'pi':
            uptime = msg['params']['uptime'] / 1000 / 60
            loads = msg['params']['loads']
            mem_info = {'used': msg['params']['memUsed'], 'percent': msg['params']['memPercent']}
            host_name = msg['params']['hostname']
            display_on_screen(uptime, loads, mem_info, host_name)
    elif msg['action'] == 3:
        display_mode = msg['params']
        pass


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

now_time = datetime.now().time()
if now_time > dateutil.parser.parse('18:30').time() or now_time < dateutil.parser.parse('7:00').time():
    GPIO.output(LED, ON)
else:
    GPIO.output(LED, OFF)

showcpu = threading.Thread(target=show_cpu_info)
showcpu.setDaemon(True)
showcpu.start()

start_listen()
