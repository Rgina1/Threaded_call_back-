import time
from Shifter import Shifter
from Bug_class import Bug
import RPi.GPIO as GPIO
import threading 
GPIO.setmode(GPIO.BCM)

try:
    Shfiter_object = Shifter(23,25,24)
    bug_object = Bug(Shfiter_object, timestep=0.1, x=3, isWrapOn=False)
    Switch = [17,27,22]

    
    
    def S1(s1):
        value = GPIO.input(s1)
        if(value):
            threading.Thread(target=bug_object.start).start()
        else:
            bug_object.stop()
    def S2(s2,bug = bug_object):
        bug.isWrapOn = not bug.isWrapOn
    def S3(s3):
        value = GPIO.input(s3)
        if (value):
            bug_object.timestep = 0.1/3
        else:
            bug_object.timestep = 0.1
    

    #Threaded Callbacks s1
    for i in range(0,len(Switch)):
        GPIO.setup(Switch[i], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    GPIO.add_event_detect(Switch[0], 
                        GPIO.BOTH, 
                        callback= S1,
                        bouncetime=200)

    #Threaded Callbacks s2
    
    GPIO.add_event_detect(Switch[1], 
                        GPIO.RISING, 
                        callback= S2,
                        bouncetime=200)
    #Threaded Callbacks s3
    
    GPIO.add_event_detect(Switch[2], 
                        GPIO.BOTH, 
                        callback=S3,
                        bouncetime=200)

    while True: pass

except KeyboardInterrupt:
    bug_object.stop()
    GPIO.cleanup()


