"""
ultra sonic sensor control in raspberry pi 4
"""
import time
import RPi.GPIO as GPIO
from GPIO_HW_control.hw_interface import HWInterface


class UltrasonicSensor(HWInterface):
    """
    
    """
    def __init__(self, us_trig_pin, us_echo_pin):
        self.us_trig_pin = us_trig_pin
        self.us_echo_pin = us_echo_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.us_trig_pin, GPIO.OUT)
        GPIO.setup(self.us_echo_pin, GPIO.IN)

    def __del__(self):
        GPIO.cleanup(self.us_trig_pin)
        GPIO.cleanup(self.us_echo_pin)

    def control(self):
        """
        desc:
        """

    def mesure_distance(self):
        """desc:

        """
        # 트리거 신호 발생
        GPIO.output(self.us_trig_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.us_trig_pin, GPIO.LOW)

        # 에코 펄스 신호 시간 측정
        pulse_start = time.time()
        pulse_end = time.time()
        while GPIO.input(self.us_echo_pin) == 0:
            pulse_start = time.time()
        while GPIO.input(self.us_echo_pin) == 1:
            pulse_end = time.time()
        # 에코 펄스 지속 시간 계산
        pulse_duration = pulse_end - pulse_start
        # 거리 계산 (음속: 343m/s, 2로 나누어야 양방향 거리)
        distance = (pulse_duration * 34300) / 2
        return distance
