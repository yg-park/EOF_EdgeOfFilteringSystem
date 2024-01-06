"""
라인을 제어하는 모듈입니다.
"""
import asyncio
import threading
import time
import cv2
from GPIO_HW_control.rc_servo_motor import RCServoMotor
from GPIO_HW_control.servo_motor import ServoMotor
from GPIO_HW_control.button import Button
from GPIO_HW_control.lcd import LCD
from Communication.image_communication import ImageCommunication
from Communication.audio_communication import AudioCommunication
from Communication.hw_control_communication import HWControlCommunication
from Audio.voice_record import AudioRecorder


class LaneController:
    """라인을 제어하기 위한 클래스입니다."""
    def __init__(self):
        self.btn_clicked_flag = False
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
        self.button_controller = Button()
        self.servo_motor = ServoMotor()
        self.lcd_controller = LCD()
        self.recorder = AudioRecorder()
        self.camera = cv2.VideoCapture(0)
        
        
    def _init_thread(self):
        self.webcam_thread = threading.Thread(target=self.send_frame_to_server)
        self.voice_thread = threading.Thread(
            target=self.record_voice_and_send_thread)
        #self.hw_control_thread = threading.Thread(target=self.hw_control)
        self.hw_control_thread = threading.Thread(target=lambda:asyncio.run(self.async_hw_control_thread()))
        self.servo_thread = threading.Thread(target=self.servo_motor.kick)
        self.listen_hw_control_thread = threading.Thread(
            target=self.hw_control_comm.receive)

    async def async_servo_handler(self):
        print("event occur")
        self.servo_motor._set_servo_angle(45)
        await asyncio.sleep(2)
        self.servo_motor._set_servo_angle(0)

    async def async_hw_control_thread(self):
        while True:
            if self.button_controller.sensingBTN() is False:
                await self.record_voice_and_send_thread()
                print("btn click")
            if self.hw_control_comm.msg == "Servo Kick":
                await self.async_servo_handler()
                self.hw_control_comm.msg = ""
            elif self.hw_control_comm.msg == "RC Start":
                self.rc_servo_motor.start()
                self.hw_control_comm.msg = ""
                self.lcd_controller.display_clear()
                self.lcd_controller.display_lcd('RCStart')
            elif self.hw_control_comm.msg == "RC Stop":
                self.rc_servo_motor.stop()
                self.hw_control_comm.msg = ""
                self.lcd_controller.display_clear()
                self.lcd_controller.display_lcd('RCStop')
            


    async def record_voice_and_send_thread(self):
        print("btn click2")
        file_path = self.recorder.start_recording()
        self.audio_comm.send_audio_file(file_path)


    def record_voice_and_send_voice_to_server(self):
        """목소리 녹음 후, 해당 오디오 파일을 서버에 전송합니다."""
        recorder = AudioRecorder()
        file_path = self.recorder.start_recording()
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
            if self.button_controller.sensingBTN() is False:
                self.btn_clicked_flag = True
                print("btn click")
            if self.hw_control_comm.msg == "Servo Kick":
                self.servo_thread.start()
                self.hw_control_comm.msg = ""
            elif self.hw_control_comm.msg == "RC Start":
                self.rc_servo_motor.start()
                self.hw_control_comm.msg = ""
                self.lcd_controller.display_clear()
                self.lcd_controller.display_lcd('RCStart')
            elif self.hw_control_comm.msg == "RC Stop":
                self.rc_servo_motor.stop()
                self.hw_control_comm.msg = ""
                self.lcd_controller.display_clear()
                self.lcd_controller.display_lcd('RCStop')

    def execute(self):
        """스레드를 실행시킵니다."""
        try:
            self.webcam_thread.start()
            self.hw_control_thread.start()
            #self.voice_thread.start()
            self.listen_hw_control_thread.start()
        finally:
            self.webcam_thread.join()
            self.hw_control_thread.join()
            #self.voice_thread.join()
            self.listen_hw_control_thread.join()
