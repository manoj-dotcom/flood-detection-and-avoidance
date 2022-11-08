from machine import Pin
import time
buzzer=Pin(6,Pin.OUT)
while(True):
    buzzer.value(1)
    time.sleep(0.2)
    buzzer.value(0)
    time.sleep(0.2)
