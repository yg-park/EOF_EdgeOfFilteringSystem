"""
RC Servo Motor를 제어하는 모듈입니다.
"""
import RPi.GPIO as GPIO


class RCServoMotor:
    """RC Servo Motor를 제어하기 위한 클래스입니다."""
    def __init__(self, RC_SERVO_PIN1, RC_SERVO_PIN2):
        self.rc_servo_1_pin = RC_SERVO_PIN1
        self.rc_servo_2_pin = RC_SERVO_PIN2
        self.running = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.rc_servo_1_pin, GPIO.OUT)
        GPIO.setup(self.rc_servo_2_pin, GPIO.OUT)

    def __del__(self):
        GPIO.cleanup(self.rc_servo_1_pin)
        GPIO.cleanup(self.rc_servo_2_pin)

    def start(self):
        """레인을 동작시킵니다."""
        self.running = True
        GPIO.output(self.rc_servo_1_pin, GPIO.HIGH)
        GPIO.output(self.rc_servo_2_pin, GPIO.HIGH)

    def stop(self):
        """레인을 정지시킵니다."""
        self.running = False
        GPIO.output(self.rc_servo_1_pin, GPIO.LOW)
        GPIO.output(self.rc_servo_2_pin, GPIO.LOW)
