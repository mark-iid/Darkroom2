from machine import Pin
import time
import sys

led = Pin(25, Pin.OUT)


# Bit masked setting
def set_bit(position, binary):
    bit_mask = 1 << position
    return bit_mask | binary


# pin definition
output_line1 = Pin(0, Pin.OUT)
input_line1 = Pin(1, Pin.IN, Pin.PULL_DOWN)
output_line2 = Pin(2, Pin.OUT)
input_line2 = Pin(3, Pin.IN, Pin.PULL_DOWN)
output_line3 = Pin(4, Pin.OUT)
input_line3 = Pin(5, Pin.IN, Pin.PULL_DOWN)
output_line4 = Pin(6, Pin.OUT)
input_line4 = Pin(7, Pin.IN, Pin.PULL_DOWN)
led.value(1)
output_line_door = Pin(10, Pin.OUT)
output_line_bookcase = Pin(11, Pin.OUT)
output_line_door.value(0)
output_line_bookcase.value(0)

while True:
    mask = 0
    output_line1.value(1)
    output_line2.value(1)
    output_line3.value(1)
    output_line4.value(1)
    if (input_line1.value()):
        mask = set_bit(0, mask)
    if (input_line2.value()):
        mask = set_bit(1, mask)
    if (input_line3.value()):
        mask = set_bit(2, mask)
    if (input_line4.value()):
        mask = set_bit(3, mask)
    print(mask)
    while True:
        v = sys.stdin.readline().strip()
        if v.lower() == "getbytes":
            break
        elif v.lower() == "door":
            output_line_door.value(1)
        elif v.lower() == "bookcase":
            output_line_bookcase.value(1)
        elif v.lower() == "reset":
            output_line_bookcase.value(0)
            output_line_door.value(0)
