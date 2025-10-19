import RPi.GPIO as GPIO
import random
from Shifter import Shifter
import time
class Bug:

    def __init__(self, __shifter, timestep=0.1, x = 3, isWrapOn=False):
        self.i = x
        self.timestep = timestep
        self.isWrapOn = isWrapOn
        self.shifter = __shifter
        self.checkForStop = True
    def start(self):
        walkValues = [x for x in range(1,(2**8)) if ((x & x-1)==0)]
        while self.checkForStop:
            time.sleep(self.timestep)
            increment = random.randint(0,1) # zero is backwards -1
            if (increment == 0):
                increment = -1

            if(self.i > 0 and self.i < len(walkValues)-1):
                self.i=self.i+increment
            elif (self.i==0):
                if(self.isWrapOn):
                    self.i=len(walkValues)-1
                else:
                    self.i=self.i+1
            elif(self.i==len(walkValues)-1):
                if(self.isWrapOn):
                    self.i= 0
                else:
                    self.i= self.i-1

            pattern = walkValues[self.i]
            
            self.shifter.shiftByte(pattern)

    def stop(self):
        self.checkForStop = False
        off = 0b00000000
        self.shifter.shiftByte(off)
        GPIO.cleanup()