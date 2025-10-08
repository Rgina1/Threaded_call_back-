import RPi.GPIO as GPIO
import time
import math
GPIO.setmode(GPIO.BCM)


pins = [int(x) for x in input(f"input the BCM numbering of the ports you'll be using: ").split(',')]
pwms = [ ]
frequency = 0.2 # Hz
Direction = True # True is forward, backwards is left

def Brightness_with_phase(pwm_objects, f, num_leds):
    phase = math.pi/11
    for pwm in pwm_objects:
        pwm.start(0)
        
    while True:
        for i in range(num_leds):
            pwm_objects[i].ChangeDutyCycle(100*math.sin(2*math.pi*f*time.time()-(Direction*i*phase))**2)

def reverse(pin):
    global Direction
    Direction = -1*Direction
    
for pin in pins:
    GPIO.setup(pin,GPIO.OUT, initial=0)
    pwm = GPIO.PWM(pin, 500)
    pwms.append(pwm) 
# creating a Brightness function


active_pin = int(input(f"input the BCM number of the pin you'll be using to reversing the direction of LEDS: "))
GPIO.setup(active_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(active_pin, 
                      GPIO.RISING, 
                      callback=reverse,
                      bouncetime=150)
try:
    Brightness_with_phase(pwms, frequency, len(pins))
except KeyboardInterrupt:
    print("\nExiting")
    pass
for pwm in pwms:
    pwm.stop()

GPIO.remove_event_detect(active_pin)
# Clean up on exit
GPIO.cleanup()





