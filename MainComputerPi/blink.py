import serial
import time

# open a serial connection
s = serial.Serial("/dev/cu.usbmodem113201", 115200)

# blink the led
while True:
    s.write(b"on\n")
    print("on")
    time.sleep(1)
    s.write(b"off\n")
    print("off")
    time.sleep(1)