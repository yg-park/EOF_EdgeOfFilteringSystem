"""
RC Servo Motor 를 제어하는 모듈입니다.
"""
import RPi.GPIO as GPIO
# GPIO.setwarnings(False)

RC_SERVO_PIN1 = 20
RC_SERVO_PIN2 = 21


class RCServoMotor:
    """RC Servo Motor를 제어하기 위한 클래스입니다."""
    def __init__(self):
        self.rc_servo_1_pin = RC_SERVO_PIN1
        self.rc_servo_2_pin = RC_SERVO_PIN2
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.rc_servo_1_pin, GPIO.OUT)
        GPIO.setup(self.rc_servo_2_pin, GPIO.OUT)
        # self.stop()

    def __del__(self):
        GPIO.cleanup(self.rc_servo_1_pin)
        GPIO.cleanup(self.rc_servo_2_pin)

    def operate(self):
        """레인을 동작시킵니다."""
        GPIO.output(self.rc_servo_1_pin, GPIO.HIGH)
        GPIO.output(self.rc_servo_2_pin, GPIO.HIGH)

    def stop(self):
        """레인을 정지시킵니다."""
        GPIO.output(self.rc_servo_1_pin, GPIO.LOW)
        GPIO.output(self.rc_servo_2_pin, GPIO.LOW)
