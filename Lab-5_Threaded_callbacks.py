import RPi.GPIO as GPIO
import time
import math
GPIO.setmode(GPIO.BCM)

pins = [int(x) for x in input(f"input the BCM numbering of the ports you'll be using: ").split(',')]
pwms = [ ]
frequency = 0.2 # Hz
direction = True # True is forward, backwards is left

for pin in pins:
    GPIO.setup(pin,GPIO.OUT, initial=0)
    pwm = GPIO.PWM(pin, 500)
    pwms.append(pwm) 
# creating a Brightness function
def Brightness(pwm_objects, f):
    for pwm in pwm_objects:
        pwm.start(0)
    while True:
        #if(time.time()-past >= wait_time):
            #past = time.time()
        pwm_objects[0].ChangeDutyCycle(100*max(0,math.sin(2*math.pi*f*time.time())))
def Brightness_with_phase(pwm_objects, f, num_leds = 10, direction=True):
    if not direction:
        phase = -math.pi/11
    for pwm in pwm_objects:
        pwm.start(0)
    while True:
        #if(time.time()-past >= wait_time):
            #past = time.time()
        for i in range(num_leds):
            pwm_objects[i].ChangeDutyCycle(100*math.sin(2*math.pi*f*time.time()-(i*phase))**2)
def reverse():
    global direction
    direction = not direction
    Brightness_with_phase(pwms, frequency, len(pins), direction)

active_pin = int(input(f"input the BCM number of the pin you'll be using to reverse the direction of the LEDS: "))
GPIO.setup(active_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(active_pin, 
                      GPIO.RISING, 
                      callback=reverse(),
                      bouncetime=200)
try:
    Brightness_with_phase(pwms, frequency, len(pins), direction)
except KeyboardInterrupt:
    print("\nExiting")
    pass
for pwm in pwms:
    pwm.stop(0)

GPIO.remove_event_detect(p)
# Clean up on exit
GPIO.cleanup()






