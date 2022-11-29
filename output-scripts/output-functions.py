import requests

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# rgb pins
GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW) #r
GPIO.setup(6, GPIO.OUT, initial=GPIO.LOW) #g
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW) #b

def activateAlert():
    GPIO.output(5, GPIO.HIGH) #r
    GPIO.output(6, GPIO.LOW) #g
    GPIO.output(17, GPIO.LOW) #b
    r = requests.get('http://dev-machine.link:5000/activate')
    print(r.status_code)

def deactivateAlert():
    GPIO.output(5, GPIO.LOW) #r
    GPIO.output(6, GPIO.HIGH) #g
    GPIO.output(17, GPIO.LOW) #b
    r = requests.get('http://dev-machine.link:5000/deactivate')
    print(r.status_code)