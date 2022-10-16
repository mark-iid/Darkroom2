import serial
import os

# Custom standalone app to unlock the door and bookcase linear actuators
battery_processor_device = "/dev/ttyACM0"  # battery processor device
serialPort = serial.Serial(battery_processor_device, 115200, timeout=0)
serialPort.write(b"door\r\n")
serialPort.write(b"bookcase\r\n")
