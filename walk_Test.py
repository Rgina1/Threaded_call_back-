from Shifter import Shifter
import random
walkValues = [x for x in range(1,(2**8)+1) if ((x & x-1)==0)] 
Shfiter_object = Shifter(23,24,25)
i = random.randint(0,len(walkValues)-1)
while True:
    increment = random.randint(0,1) # zero is backwards -1
    if (increment == 0):
        increment = -1

    if(i > 0 and i < len(walkValues)-1):
        i=i+increment
    elif (i==0):
        i=i+1
    elif(i==len(walkValues)-1):
        i=i-1
    pattern = walkValues[i]

    Shfiter_object.shiftByte(pattern)


