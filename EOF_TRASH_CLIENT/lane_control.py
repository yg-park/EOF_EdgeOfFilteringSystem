"""
ㅇ
"""
#import threading
import cv2
import time
from GPIO_HW_control.servo_motor import ServoMotor
from GPIO_HW_control.ultrasonic_sensor import UltrasonicSensor
from Comm.communication import ClientCommunication


class LaneController:
    """desc:
    
    """
    def __init__(self, pin, ip_address, port) -> None:
        """desc:
        
        """
        # self.rc_servo_motor = ???
        self.servo_motor = ServoMotor(pin["SERVO"])
        self.ultra_sonic_sensor = UltrasonicSensor(
            pin["ULTRASONIC_TRIG"], pin["ULTRASONIC_ECHO"]
            )
        self.camera = cv2.VideoCapture(0)
        # self.mic = ???
        # self.lcd = ???
        self.comm = ClientCommunication(ip_address, port["PORT_IMAGE"])
        # self.model = ???

    def __del__(self):
        self.camera.release()

    def execute(self):
        # kick_trash = threading.Thread(target=self.servo_motor.control, args=())

        while True:
            _, frame = self.camera.read()
            if frame is None:
                continue

            self.comm.send_frame(frame)
            time.sleep(1/30)