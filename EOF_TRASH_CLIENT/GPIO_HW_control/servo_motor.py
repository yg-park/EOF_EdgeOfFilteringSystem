"""
servo motor control in raspberry pi 4
"""
import time
import RPi.GPIO as GPIO
from GPIO_HW_control.hw_interface import HWInterface


class ServoMotor(HWInterface):
    """
    desc:
    """
    def __init__(self, servo_pin):
        self.servo_pin = servo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(servo_pin, 50)  # 주파수 50Hz로 PWM 생성
        self.pwm.start(0)  # PWM 시작

    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup(self.servo_pin)

    def control(self):
        """
        desc:
        """
        self.set_servo_angle(90)
        time.sleep(1)
        self.set_servo_angle(0)

    def set_servo_angle(self, angle):
        """
        desc:
        """
        duty_cycle = (angle / 18) + 2  # 각도를 PWM 듀티 사이클로 변환
        GPIO.output(self.servo_pin, True)
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(1)  # 1초 대기 (서보 모터가 동작할 시간)
        GPIO.output(self.servo_pin, False)
        self.pwm.ChangeDutyCycle(0)
