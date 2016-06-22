#!/usr/bin/env python
import signal
import sys
import time
import urllib
import urllib2
import json
import RPi.GPIO as GPIO
from settings import UPDATE_INTERVAL, RED, YELLOW, GREEN, \
        OG_API_URL, OG_API_KEY, OG_TEAMS,ON,OFF

def on(color):
    print 'on: ' + str(color)
    GPIO.output(color,ON)
    return

def off(color):
    print 'off: ' + str(color)
    GPIO.output(color,OFF)
    return

def signal_handler(signal, frame):
    print('caught sigint, exiting')
    GPIO.cleanup()
    sys.exit(0)

def set_color(color):
    return

signal.signal(signal.SIGINT, signal_handler)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(RED,GPIO.OUT)
GPIO.setup(YELLOW,GPIO.OUT)
GPIO.setup(GREEN,GPIO.OUT)

go_red=False

# prepare API request
open_request_values = {'status': 'open',
                            'teams': OG_TEAMS,
                            'apiKey': OG_API_KEY }
open_request_params = urllib.urlencode(open_request_values)

# Need a GET request, so have to put em together this way rather than data param
open_request = urllib2.Request(OG_API_URL + '/?' + open_request_params)

while True:
    go_red=False
    try:
        json_returned = urllib2.urlopen(open_request).read()
        parsed_json = json.loads(json_returned)
        print json_returned
        if not parsed_json['alerts']:
            # no alerts
            off(RED)
            off(YELLOW)
            on(GREEN)
            print "green"
        else:
            for alert in parsed_json['alerts']:
                if not alert['acknowledged']:
                    # un-acked alerts that are open!
                    go_red=True
                    break
            if go_red:
                off(GREEN)
                off(YELLOW)
                on(RED)
                print "red"
            else:
                # all open alerts are acked
                off(GREEN)
                off(RED)
                on(YELLOW)
                print "yellow"
    except urllib2.HTTPError,e:
        print e.code
        # turn all lights off, something's wrong
        off(RED)
        off(YELLOW)
        off(GREEN)
    time.sleep(UPDATE_INTERVAL)

GPIO.cleanup()
