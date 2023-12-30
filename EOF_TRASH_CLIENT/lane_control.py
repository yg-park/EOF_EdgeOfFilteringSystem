"""
ㅇ
"""
import threading
import cv2
from GPIO_HW_control.servo_motor import ServoMotor
from GPIO_HW_control.ultrasonic_sensor import UltrasonicSensor
from network.communication import Communication


class LaneController:
    """desc:
    
    """
    def __init__(self, pin, port) -> None:
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
        self.comm = Communication(port)
        # self.model = ???

    def execute(self):
        kick_trash = threading.Thread(target=self.servo_motor.control, args=())
        
        flag_detection = False

        while True:
            _, frame = self.camera.read()
            if frame is None:
                continue

            self.comm.send_image_to_server(frame)
            
            if self.ultra_sonic_sensor.control() < 8:
                flag_detection = True
            else:
                if flag_detection == True:
                    # TODO: 추론 실시 스레드 start()


                    flag_detection = False
                
                



    def sensing_distance(self):



