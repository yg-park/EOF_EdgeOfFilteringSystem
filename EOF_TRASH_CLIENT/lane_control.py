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
        LINE_BUTTON_PIN = 5
        AUDIO_BUTTON_PIN = 6
        self.rc_servo_motor = RCServoMotor()
        self.line_button_controller = Button(LINE_BUTTON_PIN)
        self.audio_button_controller = Button(AUDIO_BUTTON_PIN)
        self.servo_motor = ServoMotor()
        self.lcd_controller = LCD()
        self.recorder = AudioRecorder()
        self.camera = cv2.VideoCapture(0)
        
        
    def _init_thread(self):
        self.webcam_thread = threading.Thread(target=self.send_frame_to_server)
        self.hw_control_thread = threading.Thread(
            target=lambda:asyncio.run(self.async_hw_control_thread()))
        self.voice_thread = threading.Thread(
            target=self.record_voice_and_send_thread)
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
            if self.line_button_controller.sensingBTN() is False:
                if self.rc_servo_motor.running:
                    self.rc_servo_motor.stop()
                    self.lcd_controller.display_clear()
                    self.lcd_controller.display_lcd('RCStop')
                else:
                    self.rc_servo_motor.start()
                    self.lcd_controller.display_clear()
                    self.lcd_controller.display_lcd('RCStart')
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

    def record_voice_and_send_thread(self):
        while True:
            if self.audio_button_controller.sensingBTN() is False:
                print("btn click2")
                file_path = self.recorder.start_recording()
                self.audio_comm.send_audio_file(file_path)

    def send_frame_to_server(self):
        """웹캠으로부터 얻은 이미지 프레임을 서버로 전송합니다."""
        i = 0
        while True:
            _, frame = self.camera.read()
            if frame is None:
                continue
            self.image_comm.send_frame(frame)
            time.sleep(1/30)
            print(i)
            i += 1

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
