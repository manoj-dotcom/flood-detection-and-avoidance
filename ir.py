from machine import Pin
import time
ir=Pin(2,Pin.IN)
buzzer=Pin(6,Pin.OUT)
while(True):
    x=ir.value()
    if(x==0):
        print("obstacle")
        buzzer.value(1)
        time.sleep(1)
    else:
        print("No obstacle")
        buzzer.value(0)
        time.sleep(1)
    
