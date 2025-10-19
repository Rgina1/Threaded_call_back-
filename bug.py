import time
from Shifter import Shifter
from Bug_class import Bug
import RPi.GPIO as GPIO


try:
    bug_object = Bug(Shfiter_object, timestep=0.5, x=3, isWrapOn=True)
    s1,s2,s3 = 1,2,3

    def S1_stop(s1):
        bug_object.stop()
    def S1(s1):
        bug_object.start()
    def S2(s2):
        bug_object.attribute4 = not bug_object.attribute4
    def S3(s3):
        bug_object.attribute2 = bug_object.attribute2/3
    def S3_off(s3):
        bug_object.attribute2 = 3*bug_object.attribute2

    #Threaded Callbacks s1
    
    GPIO.setup(s1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(s1, 
                        GPIO.RISING, 
                        callback= S1(),
                        bouncetime=200)
       
    GPIO.add_event_detect(s1, 
                        GPIO.FALLING, 
                        callback= S1_stop(),
                        bouncetime=200)
    GPIO.setup(s1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(s1, 
                        GPIO.RISING, 
                        callback= S1(),
                        bouncetime=200)
    #Threaded Callbacks s2
    
    GPIO.setup(s2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(s2, 
                        GPIO.RISING, 
                        callback= S2(),
                        bouncetime=200)
    #Threaded Callbacks s3
    
    GPIO.setup(s3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(s3, 
                        GPIO.RISING, 
                        callback=S3(),
                        bouncetime=200)
    GPIO.add_event_detect(s3, 
                        GPIO.FALLING, 
                        callback=S3(),
                        bouncetime=200)
except KeyboardInterrupt:
    GPIO.cleanup()

