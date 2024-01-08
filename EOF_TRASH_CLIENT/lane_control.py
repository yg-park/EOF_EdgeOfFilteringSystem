"""
라인을 제어하는 모듈입니다.
"""
import asyncio
import threading
import time
import cv2
import RPi.GPIO as GPIO

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
        self.lane_btn_flag = False
        self.audio_btn_flag = False
        self.LANE_BUTTON_PIN = 5
        self.AUDIO_BUTTON_PIN = 6
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
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LANE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.AUDIO_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.LANE_BUTTON_PIN, GPIO.FALLING, callback=self.toggle_rc_servo_motor, bouncetime=1600)
        GPIO.add_event_detect(self.AUDIO_BUTTON_PIN, GPIO.FALLING, callback=self.record_voice_and_send, bouncetime=8000)

        # self.line_button_controller = Button(LINE_BUTTON_PIN)
        # self.audio_button_controller = Button(AUDIO_BUTTON_PIN)
        self.rc_servo_motor = RCServoMotor()
        self.servo_motor = ServoMotor()
        self.lcd_controller = LCD()
        self.recorder = AudioRecorder()
        self.camera = cv2.VideoCapture(0)
        
        
    def _init_thread(self):
        self.webcam_thread = threading.Thread(target=self.send_frame_to_server)
        self.listen_hw_control_thread = threading.Thread(target=self.hw_control_comm.receive)
        self.hw_control_thread = threading.Thread(target=lambda:asyncio.run(self.async_hw_control_thread()))

    async def async_servo_handler(self):
        print("event occur")
        self.servo_motor._set_servo_angle(45)
        await asyncio.sleep(2)
        self.servo_motor._set_servo_angle(0)


    async def async_hw_control_thread(self):
        while True:
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

    def send_frame_to_server(self):
        """웹캠으로부터 얻은 이미지 프레임을 서버로 전송합니다."""
        while True:
            _, frame = self.camera.read()
            if frame is None:
                continue
            self.image_comm.send_frame(frame)
            time.sleep(1/30)

    def toggle_rc_servo_motor(self, channel):  # 반드시 channel 파라미터를 줘야함
        print("뭐야 대체")
        #self.lane_btn_flag = not self.lane_btn_flag
        if self.rc_servo_motor.running:
            self.rc_servo_motor.stop()
            self.lcd_controller.display_clear()
            self.lcd_controller.display_lcd('RCStop')
        else:
            self.rc_servo_motor.start()
            self.lcd_controller.display_clear()
            self.lcd_controller.display_lcd('RCStart')

        """
        if self.lane_btn_flag:
            if self.rc_servo_motor.running:
                self.rc_servo_motor.stop()
                self.lcd_controller.display_clear()
                self.lcd_controller.display_lcd('RCStop')
            else:
                self.rc_servo_motor.start()
                self.lcd_controller.display_clear()
                self.lcd_controller.display_lcd('RCStart')
            GPIO.remove_event_detect(self.LANE_BUTTON_PIN)
            GPIO.add_event_detect(self.LANE_BUTTON_PIN, GPIO.RISING, callback=self.toggle_rc_servo_motor, bouncetime=400)            
        else:
            if self.rc_servo_motor.running:
                self.rc_servo_motor.stop()
                self.lcd_controller.display_clear()
                self.lcd_controller.display_lcd('RCStop')
            else:
                self.rc_servo_motor.start()
                self.lcd_controller.display_clear()
                self.lcd_controller.display_lcd('RCStart')
            GPIO.remove_event_detect(self.LANE_BUTTON_PIN)
            GPIO.add_event_detect(self.LANE_BUTTON_PIN, GPIO.FALLING, callback=self.toggle_rc_servo_motor, bouncetime=400)  
        """

    def record_voice_and_send(self,channel):  # 반드시 channel 파라미터를 줘야함
        print("여길왜또와")

        file_path = self.recorder.start_recording()
        self.audio_comm.send_audio_file(file_path)
        
        """
        self.audio_btn_flag = not self.audio_btn_flag

        if self.audio_btn_flag:
            file_path = self.recorder.start_recording()
            self.audio_comm.send_audio_file(file_path)
            GPIO.remove_event_detect(self.AUDIO_BUTTON_PIN)
            GPIO.add_event_detect(self.AUDIO_BUTTON_PIN, GPIO.RISING, callback=self.record_voice_and_send, bouncetime=400)
        else:
            # file_path = self.recorder.start_recording()
            # self.audio_comm.send_audio_file(file_path)
            GPIO.remove_event_detect(self.AUDIO_BUTTON_PIN)
            GPIO.add_event_detect(self.AUDIO_BUTTON_PIN, GPIO.FALLING, callback=self.record_voice_and_send, bouncetime=400)
        """

    def execute(self):
        """스레드를 실행시킵니다."""
        try:
            self.webcam_thread.start()
            self.listen_hw_control_thread.start()
            self.hw_control_thread.start()
            
        finally:
            self.webcam_thread.join()
            self.listen_hw_control_thread.join()
            self.hw_control_thread.join()
