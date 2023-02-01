#!/usr/bin/env python3
#-- coding: utf-8 --
import RPi.GPIO as GPIO
import time

#Set function to calculate percent from angle
def angle_to_percent (angle) :
    if angle > 180 or angle < 0 :
        return False

    start = 3
    end = 12.5
    ratio = (end - start)/180 #Calcul ratio from angle to percent

    angle_as_percent = angle * ratio

    return start + angle_as_percent



 #Use Board numerotation mode
# GPIO.setwarnings(False) #Disable warnings

#Use pin 12 for PWM signal

cnt = 0;

# 
# while True : 
#     i=1
#     if i <1:
#         #Init at 0°
#         pwm.start(angle_to_percent(0))
#         time.sleep(1)
#         i = 1
#     if i >=1 :
#         #Go at 90°
#         pwm.start(angle_to_percent(180))
#         time.sleep(1)
#         i = 0
    

def motorOpen():
    pwm_gpio1 = 12
    pwm_gpio2 = 16
    frequence = 50
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwm_gpio1, GPIO.OUT)
    GPIO.setup(pwm_gpio2, GPIO.OUT)
    pwm1 = GPIO.PWM(pwm_gpio1, frequence)
    pwm2 = GPIO.PWM(pwm_gpio2, frequence)
    
    pwm1.start(3.0)
    pwm2.start(3.0)
    pwm1.ChangeDutyCycle(3.0)
    pwm2.ChangeDutyCycle(8.0)
    time.sleep(2)
    pwm1.ChangeDutyCycle(8.0)
    pwm2.ChangeDutyCycle(3.0)
    time.sleep(1)
    pwm1.stop()
    pwm2.stop()
    
def motorClose():
    pwm_gpio = 12
    frequence = 50
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwm_gpio, GPIO.OUT)
    pwm = GPIO.PWM(pwm_gpio, frequence)
    
    time.sleep(1)
    pwm.stop()

