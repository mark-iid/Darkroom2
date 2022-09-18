from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 4, 20)
lcd.clear
lcd.putstr("      LAB DOOR")
lcd.move_to(0,1)
lcd.putstr("   Status: Locked")
lcd.move_to(0,2)
lcd.putstr("   Enter Keycode")
lcd.move_to(8,3)
lcd.putstr("____")
lcd.move_to(8,3)
lcd.blink_cursor_on()