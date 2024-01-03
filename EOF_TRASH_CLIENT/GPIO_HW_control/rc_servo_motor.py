"""
rc servo motor control in raspberry pi 4
"""
import RPi.GPIO as GPIO
from GPIO_HW_control.hw_interface import HWInterface
#GPIO.setwarnings(False)

class RCServoMotor(HWInterface):
    """
    desc:
    """
    def __init__(self, rc_servo_1_pin, rc_servo_2_pin):
        self.rc_servo_1_pin = rc_servo_1_pin
        self.rc_servo_2_pin = rc_servo_2_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(rc_servo_1_pin, GPIO.OUT)
        GPIO.setup(rc_servo_2_pin, GPIO.OUT)
        # self.stop()

    def __del__(self):
        GPIO.cleanup(self.rc_servo_1_pin)
        GPIO.cleanup(self.rc_servo_2_pin)

    def control(self):
        """
        desc:
        """
        
    def start(self):
        """레인을 동작시킵니다."""
        GPIO.output(self.rc_servo_1_pin, GPIO.HIGH)
        GPIO.output(self.rc_servo_2_pin, GPIO.HIGH)

    def stop(self):
        """레인을 정지시킵니다."""
        GPIO.output(self.rc_servo_1_pin, GPIO.LOW)
        GPIO.output(self.rc_servo_2_pin, GPIO.LOW)
