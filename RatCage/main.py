from machine import I2C, Pin, PWM

MID = 1500000 # midpoint of servo motor
MIN = 400000 # minpoint of servo motor
MAX = 2100000 # maxpoint of servo motor

# servo motor setup
pwm = PWM(Pin(2))
pwm.freq(50)
pwm.duty_ns(MIN)


output_line1 = Pin(3, Pin.OUT)
input_line1 = Pin(4, Pin.IN, Pin.PULL_DOWN)

while True:
    output_line1.value(1)
    pwm.duty_ns(MIN)
    while input_line1.value():
        pwm.duty_ns(MAX)
