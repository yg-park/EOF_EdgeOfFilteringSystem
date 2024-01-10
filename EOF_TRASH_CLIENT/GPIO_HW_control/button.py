"""
버튼과 관련된 작업을 수행하는 모듈입니다.
"""
import RPi.GPIO as GPIO
import time


class Button:
    """버튼 입력을 받기 위한 클래스입니다."""
    def __init__(self, BUTTON_PIN):
        self.BUTTON_PIN = BUTTON_PIN
        self.lastButtonState = GPIO.HIGH
        self.lastDebounceTime = 0
        self.debounceDelay = 0.2

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __del__(self):
        GPIO.cleanup(self.BUTTON_PIN)

    def sensingBTN(self):
        """디바운스를 적용하여 버튼 입력을 감지합니다."""
        curr_state = GPIO.input(self.BUTTON_PIN)
        if curr_state == GPIO.LOW and self.lastButtonState == GPIO.HIGH:
            self.lastDebounceTime = time.time()
            self.lastButtonState = GPIO.LOW
            return True
        elif curr_state == GPIO.HIGH and self.lastButtonState == GPIO.LOW:
            if (time.time() - self.lastDebounceTime) > self.debounceDelay:
                self.lastButtonState = GPIO.HIGH
                return False
        return True
