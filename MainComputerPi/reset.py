import serial
import os

# Standalone app to reset the locks
battery_processor_device = "/dev/ttyACM0"  # battery processor device
serialPort = serial.Serial(battery_processor_device, 115200, timeout=0)
serialPort.write(b"reset\r\n")
