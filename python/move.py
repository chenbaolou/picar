# -*- coding: utf-8 -*-
# Car's movement control (forward, back, left, right, brake)
# motor control

simulate_mode = True
debug_mode = True

if not simulate_mode:
    import RPi.GPIO as GPIO
    import Adafruit_PCA9685
import time
import math

ANGLE_MAX = 460
ANGLE_MIDDLE = 360
ANGLE_MIN = 260

SPEED_MAX = 40
SPEED_MIN = 0

if not simulate_mode:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

def isfloat(s):
    try:
        n = eval(s)
    except:
        return False
    
    if isinstance(n, float):
        return True
    else:
        return False

class CarMove(object):
    def __init__(self):
        GPIO_motor_3 = 18  # GPIO setting (BCM coding)
        AIN1 = 22
        AIN2 = 27

        GPIO_motor_4 = 23
        BIN1 = 25
        BIN2 = 24

        self.speed = 0
        self.angle = 0

        if not simulate_mode:

            #初始化电机
            GPIO.setup(GPIO_motor_3, GPIO.OUT)  # GPIO input/output definiation
            GPIO.setup(AIN1,GPIO.OUT)
            GPIO.setup(AIN2,GPIO.OUT)
            
            GPIO.setup(GPIO_motor_4, GPIO.OUT)
            GPIO.setup(BIN1,GPIO.OUT)
            GPIO.setup(BIN2,GPIO.OUT)

            self.motor_3 = GPIO.PWM(GPIO_motor_3, 500)  # PWM initialization: 500 Hz
            self.motor_4 = GPIO.PWM(GPIO_motor_4, 500)

            self.motor_3.start(0)  # motors start
            self.motor_4.start(0)

            #初始化舵机
            self.servo_pwm = Adafruit_PCA9685.PCA9685()
            self.servo_pwm.set_pwm_freq(60)
            self.servo_pwm.set_pwm(0,0, 360)

    def forward(self, speed):
        will_speed = 0
        
        if isfloat(speed):
            will_speed = int(math.ceil(float(speed) * SPEED_MAX))
        elif speed.isdigit():
            if int(speed) == 0:
                will_speed = SPEED_MIN
            else:
                will_speed = SPEED_MAX * int(speed)
        else:
            will_speed = SPEED_MIN

        if will_speed == self.speed:
            return 0

        #切换方向
        if (will_speed == abs(will_speed))  !=  (self.speed == abs(self.speed)):
            if will_speed > 0:
                if not simulate_mode:
                    GPIO.output(self.AIN1,True)
                    GPIO.output(self.AIN2,False)
                    GPIO.output(self.BIN1,True)
                    GPIO.output(self.BIN2,False)
                if debug_mode:
                    print("change direction to up")
            else:
                if not simulate_mode:
                    GPIO.output(self.AIN1,False)
                    GPIO.output(self.AIN2,True)
                    GPIO.output(self.BIN1,False)
                    GPIO.output(self.BIN2,True)
                if debug_mode:
                    print("change direction to back")

        self.speed = will_speed

        if not simulate_mode:
            self.motor_3.ChangeDutyCycle(speed)  # set the duty circle (range: 0~100)
            self.motor_4.ChangeDutyCycle(speed)

        if debug_mode:
            print("speed:", self.speed)

    def turn(self, angle):
        
        will_angle = 0

        if isfloat(angle):
            will_angle = ANGLE_MIDDLE + int(math.ceil(float(angle) * (ANGLE_MAX - ANGLE_MIN)/2))
        elif angle.isdigit():
            if int(angle) == 1:
                will_angle = SPEED_MAX
            elif int(angle) == -1:
                will_angle = ANGLE_MIN
            else:
                will_angle = ANGLE_MIDDLE
        else:
            will_angle = ANGLE_MIDDLE
        
        if will_angle == self.angle:
            return 0
        
        if not simulate_mode:
            self.servo_pwm.set_pwm(0, 0, will_angle)
        
        self.angle = will_angle

        if debug_mode:
            print("angle:", self.angle)

    def stop(self):
        self.motor_3.stop()
        self.motor_4.stop()

if __name__ == '__main__':
    try:
        car = CarMove()
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        car.stop()
        GPIO.cleanup()
