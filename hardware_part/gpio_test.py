# import RPi.GPIO as gpio
import time
from gpiozero import LED
wr = LED(2)

for index in range(10000):
    time.sleep(0.01)
    wr.on()
    time.sleep(0.01)
    wr.off()
    if index % 100 == 0:
        print("100 term end ...")
print("end .")