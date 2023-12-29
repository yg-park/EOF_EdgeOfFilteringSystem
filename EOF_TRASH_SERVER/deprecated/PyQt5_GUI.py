import cv2
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from GPIO_HW_control.servo_motor import ServoMotor
from GPIO_HW_control.ultrasonic_sensor import UltrasonicSensor
from network.tcp_client import TCPClient
from network.udp_client import UDPClient
from model.bottle_classifier import BottleClassifier

# 전역 변수
flag_us = False
inference_status = -1


class MainWorkerThread(QThread):
    
    def __init__(self):
        super().__init__()
        self.cap = self._initCam()
        self.bottle_classifier = self._initModel()
        self.tcp_client, self.udp_client = self._initNetwork()

    
    def _initCam(self):
        cap = cv2.VideoCapture(0)

        if cap.isOpened():
            return cap
        else:
            print("Error: Could not open webcam.")
            return
        

    def _initModel(self):
        model_path = './model/eof_bottle_classification_model.pth'
        bottle_classifier = BottleClassifier(model_path)
        return bottle_classifier


    def _initNetwork(self):
        TCP_IP = "10.10.15.58"
        TCP_PORT = 8888
        UDP_IP = "10.10.15.58"
        UDP_PORT = 12345
        tcp_client = TCPClient(TCP_IP, TCP_PORT)
        udp_client = UDPClient(UDP_IP, UDP_PORT)
        return tcp_client, udp_client


    def run(self):
        global flag_us
        global inference_status

        while True:
            ret, frame = self.cap.read()
            self.udp_client.send_webcam_frame_to_server(frame) # 여기서 udp를 통해 서버로 frame 전송

            if flag_us == True:
                result = self.bottle_classifier.classify(frame)
                print("모델 inference 발생")
                
                if result == self.bottle_classifier.class_name[0]: # 'nl_bottle'
                    inference_status = 0
                    print(f"추론 완료... inference_status = {inference_status}")
                    self.tcp_client.send_result_to_server(0) # 여기서 tcp를 통해서 서버로 0 전송
                    time.sleep(1)

                elif result == self.bottle_classifier.class_name[1]: # 'yl_bottle'
                    inference_status = 1
                    print(f"추론 완료... inference_status = {inference_status}")
                    self.tcp_client.send_result_to_server(1) # 여기서 tcp를 통해서 서버로 1 전송
                    time.sleep(1)
                    
                else:
                    pass
                
                flag_us = False
                pass


class UltrasonicThread(QThread):
    
    us_trig_pin = 2 # 초음파센서 GPIO: 트리거 핀
    us_echo_pin = 3 # 초음파센서 GPIO: 에코 핀

    def __init__(self):
        super().__init__()
        self.us = UltrasonicSensor(self.us_trig_pin, self.us_echo_pin)


    def run(self):
        """1초에 한번씩 초음파 센서가 거리를 측정합니다."""
        global flag_us

        last_execution_time = time.time()
        while True:
            current_time = time.time()
            if current_time - last_execution_time >= 1:
                distance = self.us.measure_distance()
                print(f"Distance: {distance:.2f} cm")

                if distance < 8:
                    flag_us = True
                    print("물체감지")

                last_execution_time = current_time


class ServomotorThread(QThread):
    
    servo1_pin = 23 # 서보모터1 GPIO

    def __init__(self):
        super().__init__()
        self.servo = ServoMotor(self.servo1_pin)


    def run(self):
        global inference_status

        while True:
            """
            if 모델 추론 결과 == label:
                self.servo
            """
            if inference_status == 0:
                self.kick()
                inference_status = -1

            elif inference_status == 1:
                inference_status = -1
                pass
            
    
    def kick(self):
        self.servo.set_servo_angle(90)
        last_execution_time = time.time()
        while True:
            current_time = time.time()
            if current_time - last_execution_time >= 1:
                self.servo.set_servo_angle(0)
                break


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "EOF SeparateTrashCollection - Client"
        self.top = 100
        self.left = 100
        self.width = 640
        self.height = 580

        self.initUI()
        self.initThread()

    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


    def initThread(self):
        # 웹캠 스레드 생성
        self.thread_mainWorker = MainWorkerThread()
        self.thread_mainWorker.start()
        
        # 초음파센서 스레드 생성
        self.thread_us = UltrasonicThread()
        self.thread_us.start()

        # 서보모터 스레드 생성
        self.thread_servo = ServomotorThread()
        self.thread_servo.start()
