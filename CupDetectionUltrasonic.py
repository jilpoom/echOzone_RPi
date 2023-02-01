# cup detection ultrasonic sensor
import RPi.GPIO as gpio
import time

def isCupDetect():
    gpio.setmode(gpio.BCM)
    trig = 13
    echo = 19
    distance = 0
    pulse_start = 0;
    pulse_end = 0;
    cupDetectCheck = 0;
    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN)
    while True :
        gpio.output(trig, False)
        time.sleep(0.3)         
        gpio.output(trig, True)
        time.sleep(0.1)
        gpio.output(trig, False)
            
        while gpio.input(echo) == 0:
            pulse_start = time.time()
                
        while gpio.input(echo) == 1 :
            pulse_end = time.time()
                
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)

        if distance < 5:
            print(f'now distance : {distance}')
            cupDetectCheck += 1  
            
        if(cupDetectCheck == 5):
            print('cup detection!')
            cupDetectCheck = 0
            gpio.cleanup()
            return True

