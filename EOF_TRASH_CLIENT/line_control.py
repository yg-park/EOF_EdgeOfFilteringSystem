"""
라인을 제어하는 모듈입니다.
"""
import threading
import time
import cv2
from GPIO_HW_control.rc_servo_motor import RCServoMotor
from GPIO_HW_control.servo_motor import ServoMotor
from Communication.send_image import ImageCommunication
from Communication.send_audio import AudioCommunication
from Communication.rcv_control_order import HWControlCommunication
from Audio.voice_record import AudioRecorder


class LineController:
    """라인을 제어하기 위한 클래스입니다."""
    def __init__(self):
        self._init_comm()
        self._init_hw()
        self._init_thread()

    def __del__(self):
        self.camera.release()
        
    def _init_comm(self):
        self.image_comm = ImageCommunication()
        self.audio_comm = AudioCommunication()
        self.hw_control_comm = HWControlCommunication()
    
    def _init_hw(self):
        self.rc_servo_motor = RCServoMotor()
        self.servo_motor = ServoMotor()
        self.camera = cv2.VideoCapture(0)

    def _init_thread(self):
        self.webcam_thread = threading.Thread(target=self.send_frame_to_server)
        self.voice_thread = threading.Thread(
            target=self.record_voice_and_send_voice_to_server)
        self.hw_control_thread = threading.Thread(target=self.hw_control)
        self.servo_thread = threading.Thread(target=self.servo_motor.kick)
        self.listen_hw_control_thread = threading.Thread(
            target=self.hw_control_comm.receive)

    def record_voice_and_send_voice_to_server(self):
        """목소리 녹음 후, 해당 오디오 파일을 서버에 전송합니다."""
        recorder = AudioRecorder()
        file_path = recorder.start_recording()
        self.audio_comm.send_audio_file(file_path)

    def send_frame_to_server(self):
        """웹캠으로부터 얻은 이미지 프레임을 서버로 전송합니다."""
        while True:
            _, frame = self.camera.read()
            if frame is None:
                continue
            self.image_comm.send_frame(frame)
            time.sleep(1/60)

    def hw_control(self):
        """서버로부터 HW를 제어하는 통신을 받아 HW를 제어합니다."""
        while True:
            if self.listen_hw_control_thread.msg == "Servo Kick":
                self.servo_thread.start()
                self.listen_hw_control_thread.msg = ""
            elif self.listen_hw_control_thread.msg == "RC Start":
                self.rc_servo_motor.operate()
                self.listen_hw_control_thread.msg = ""
            elif self.listen_hw_control_thread.msg == "RC Stop":
                self.rc_servo_motor.stop()
                self.listen_hw_control_thread.msg = ""

    def execute(self):
        """스레드를 실행시킵니다."""
        try:
            self.webcam_thread.start()
            self.hw_control_thread.start()
            self.voice_thread.start()
            self.listen_hw_control_thread.start()
        finally:
            self.webcam_thread.join()
            self.hw_control_thread.join()
            self.voice_thread.join()
            self.listen_hw_control_thread.join()
