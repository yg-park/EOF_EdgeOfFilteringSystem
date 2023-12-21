"""
gpio control in raspberry pi 4
"""
import RPi.GPIO as GPIO
import time

us_trig_pin = 2  # 트리거 핀
us_echo_pin = 3  # 에코 핀
servo_pin = 23




class gpio_control:
    def __init__(self,us_trig_pin,us_echo_pin,servo_pin):
        self.us_trig_pin=us_trig_pin
        self.us_echo_pin=us_echo_pin
        self.servo_pin=servo_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin, GPIO.OUT)
        GPIO.setup(self.us_trig_pin, GPIO.OUT)
        GPIO.setup(self.us_echo_pin, GPIO.IN)
        self.pwm = GPIO.PWM(servo_pin, 50)# 주파수 50Hz로 PWM 생성
        # PWM 설정
        self.pwm.start(0)  # PWM 시작




    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup()




    #ultra sonic measure function
    def measure_distance(self):
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

    """servo motor control function"""
    def set_servo_angle(self,angle):
        duty_cycle = (angle / 18) + 2  # 각도를 PWM 듀티 사이클로 변환
        GPIO.output(self.servo_pin, True)
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(1)  # 1초 대기 (서보 모터가 동작할 시간)
        GPIO.output(self.servo_pin, False)
        self.pwm.ChangeDutyCycle(0)


gpio = gpio_control(us_trig_pin,us_echo_pin,servo_pin)
while True:
    gpio.set_servo_angle(90)
    time.sleep(2)
    gpio.set_servo_angle(0)
    time.sleep(2)
    distance = gpio.measure_distance()
    print(f"Distance: {distance:.2f} cm")
    time.sleep(0.1)
