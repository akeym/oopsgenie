#!/usr/bin/env python

# Make a traffic light display current alert state from OpsGenie
# uses api v2
import requests
import signal
import sys
import time
from urllib.request import urlopen

import json
import RPi.GPIO as GPIO
from settings import UPDATE_INTERVAL, RED, YELLOW, GREEN, \
        OG_API_URL, OG_API_KEY, OG_TEAMS,ON,OFF

def on(color):
    print('on: ' + str(color))
    GPIO.output(color,ON)
    return

def off(color):
    print('off: ' + str(color))
    GPIO.output(color,OFF)
    return

def signal_handler(signal, frame):
    print('caught sigint, exiting')
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(RED,GPIO.OUT)
GPIO.setup(YELLOW,GPIO.OUT)
GPIO.setup(GREEN,GPIO.OUT)

auth_headers = {'Authorization': "GenieKey {0}".format(OG_API_KEY)}

open_params = {'query': "status:open teams:{0}".format(OG_TEAMS)}
acked_params = {'query': "status:open acknowledged:true teams:{0}".format(OG_TEAMS)}

while True:
    try:
        r = requests.get(url=OG_API_URL, headers=auth_headers, params=open_params)
        parsed_json = json.loads(r.content)
        print(r.content)
        if parsed_json['data']['count'] == 0:
            off(RED)
            off(YELLOW)
            on(GREEN)
            print('green')
        else:
            r = requests.get(url=OG_API_URL, headers=auth_headers, params=acked_params)
            parsed_json = json.loads(r.content)
            if parsed_json['data']['count'] == 0:
                off(GREEN)
                off(YELLOW)
                on(RED)
                print('red')
            else:
                off(GREEN)
                off(RED)
                on(YELLOW)
                print('yellow')
    except requests.exceptions.RequestException as e:
        print(e)
        off(RED)
        off(YELLOW)
        off(GREEN)
    time.sleep(UPDATE_INTERVAL)

GPIO.cleanup()
