import utime
from machine import I2C, Pin, Timer, PWM
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 0x27 # i2c address for display
I2C_NUM_ROWS = 2 # number of rows in display
I2C_NUM_COLS = 16 # number of columns in display

MID = 1500000 # midpoint of servo motor
MIN = 1000000 # minpoint of servo motor
MAX = 2000000 # maxpoint of servo motor

KEY_UP   = const(0) # key not pressed
KEY_DOWN = const(1) # key pressed
keys = [['1', '4', '7', '*'], ['2', '5', '8', '0'], ['3', '6', '9', '#'], ['A', 'B', 'C', 'D']] # key array

rows = [8,9,10,11] # key row gpio pins
cols = [12,13,15,16] # key columm gpio pins
row_pins = [Pin(pin_name, mode=Pin.OUT) for pin_name in rows] 
col_pins = [Pin(pin_name, mode=Pin.IN, pull=Pin.PULL_DOWN) for pin_name in cols]

# keypress timer poller
timer_keys = Timer()

# display setup
i2c = I2C(0, sda=machine.Pin(4), scl=machine.Pin(5), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)    

# servo motor setup
pwm = PWM(Pin(2))
pwm.freq(50)
pwm.duty_ns(MIN)

# initial password settings
passcode = "1234" 
entered_passcode = ""

# Initialize keypad
def InitKeypad():
    for row in range(0,4):
        for col in range(0,4):
            row_pins[row].low()


# Poll for keypad press and process
def PollKeypad(timer):
    global entered_passcode # reference current entered passcode
    key = None
    for row in range(4):
        for col in range(4):
            # Set the current row to high
            row_pins[row].high()
            # Check for key pressed events
            if col_pins[col].value() == KEY_DOWN:
                key = KEY_DOWN
            if col_pins[col].value() == KEY_UP:
                key = KEY_UP
            row_pins[row].low()
            if key == KEY_DOWN:
                if keys[row][col] == 'C':
                    entered_passcode = ""
                    lcd.clear()
                    lcd.putstr("Enter Keycode")
                    lcd.move_to(0,1)
                    lcd.show_cursor()
                    lcd.blink_cursor_on()
                else:
                    lcd.putchar(keys[row][col])
                    entered_passcode = entered_passcode + keys[row][col]
                    last_key_press = keys[row][col]


# main loop
def keypadlock_main():
    InitKeypad()
    global entered_passcode
    print("Running keypadlock_main")
    lcd.putstr("Enter Keycode")
    lcd.move_to(0,1)
    lcd.show_cursor()
    lcd.blink_cursor_on()
    timer_keys.init(freq=2, mode=Timer.PERIODIC, callback=PollKeypad)
    while True:
        while entered_passcode != passcode:
            if len(entered_passcode) > 3:
                utime.sleep(1)
                lcd.clear()
                lcd.putstr("Incorrect")
                lcd.move_to(0,1)
                lcd.putstr("Keycode")
                utime.sleep(2)
                lcd.clear()
                lcd.putstr("Enter Keycode")
                lcd.move_to(0,1)
                lcd.show_cursor()
                lcd.blink_cursor_on()
                entered_passcode = ""
        utime.sleep(1)
        lcd.clear()
        lcd.putstr("Correct")
        lcd.move_to(0,1)
        lcd.putstr("Keycode")
        pwm.duty_ns(MAX)
        entered_passcode = ""
        while entered_passcode != 'D':
            if len(entered_passcode) > 1:
                entered_passcode = ""
        pwm.duty_ns(MIN)
        lcd.clear()
        lcd.putstr("Enter Keycode")
        lcd.move_to(0,1)
        lcd.show_cursor()
        lcd.blink_cursor_on()
        entered_passcode = ""
        
    
    pwm.stop()

if __name__ == "__main__":
    keypadlock_main()


