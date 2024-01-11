"""
서보모터를 제어하는 모듈입니다.
"""
import time
import RPi.GPIO as GPIO


class ServoMotor:
    """서보모터를 제어하는 클래스입니다."""
    def __init__(self, SERVO_PIN):
        self.servo_pin = SERVO_PIN
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servo_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.servo_pin, 50)  # 주파수 50Hz로 PWM 생성
        self.pwm.start(0)  # PWM 시작

    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup(self.servo_pin)

    def _set_servo_angle(self, angle):
        duty_cycle = (angle / 18) + 2  # 각도를 PWM 듀티 사이클로 변환
        GPIO.output(self.servo_pin, True)
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.2)  # 1초 대기 (서보 모터가 동작할 시간)
        GPIO.output(self.servo_pin, False)
        self.pwm.ChangeDutyCycle(0)

    def kick(self):
        """서보모터를 작동하여 kick합니다."""
        self._set_servo_angle(45)
        time.sleep(2)
        self._set_servo_angle(0)
