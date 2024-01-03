"""
ㅇ
"""
import threading
import time
import cv2
from GPIO_HW_control.rc_servo_motor import RCServoMotor
from GPIO_HW_control.servo_motor import ServoMotor
from Comm.communication import ClientCommunication
from Comm.send_audio import AudioCommunication
from audio.voice_record import AudioRecorder

class LaneController:
    """desc:
    
    """
    def __init__(self, pin, ip_address, port) -> None:
        """desc:
        
        """
        self.rc_servo_motor = RCServoMotor(pin["RC_SERVO_1"], pin["RC_SERVO_2"])
        self.servo_motor = ServoMotor(pin["SERVO"])
        self.camera = cv2.VideoCapture(0)
        self.ip_address = ip_address
        self.port = port
        self._init_thread()
        
        # self.mic = ???
        # self.lcd = ???

    def __del__(self):
        self.camera.release()

    def _init_thread(self):
        self.comm = ClientCommunication(self.ip_address, self.port["PORT_IMAGE"])
        self.webcam_thread = threading.Thread(target=self.send_webcam_thread)
        self.voice_thread = threading.Thread(target=self.send_voice_thread)
        self.HW_thread = threading.Thread(target=self.rcv_HW_comm)
        self.servo_thread = threading.Thread(target=self.servo_motor.kick)
    
    def send_voice_thread(self):
        recorder = AudioRecorder()
        recorder.start_recording()
        time.sleep(5)
        recorder.stop_recording()

        audio_sender = AudioCommunication(self.ip_address, self.port["PORT_VOICE"])
        audio_sender.send_audio_file()

    def send_webcam_thread(self):
        while True:
            _, frame = self.camera.read()
            if frame is None:
                continue
            self.comm.send_frame(frame)
            time.sleep(1/60)        
            
    def rcv_HW_comm(self):
        """
        hw관련 서버로부터 통신 받는 쓰레드 함수
        서보모터(1)/rc서보모터 on(2) off(3)
        """
        msg = '2'
        while True:
            # TODO: TCPIP 통신 servo 제어 문자가 오면 ->HW제어
            # if 수신받은 메시지 == ' ':
            if msg == '1':
                self.servo_thread.start()
            elif msg == '2':
                self.rc_servo_motor.start()
            elif msg == '3':
                self.rc_servo_motor.stop()
    
    

    def execute(self):
        try:
            self.webcam_thread.start()
            self.HW_thread.start()
            self.voice_thread.start()
        finally:
            self.webcam_thread.join()
            self.HW_thread.join()
            self.voice_thread.join()
