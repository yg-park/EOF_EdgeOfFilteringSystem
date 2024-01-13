"""
라인을 제어하는 모듈입니다.
"""
import time
import threading
import configparser

import cv2
import pygame
import RPi.GPIO as GPIO
from gtts import gTTS

from GPIO_HW_control.rc_servo_motor import RCServoMotor
from GPIO_HW_control.servo_motor import ServoMotor
from GPIO_HW_control.button import Button
from GPIO_HW_control.lcd import LCD
from Communication.image_communication import ImageCommunication
from Communication.audio_communication import AudioCommunication
from Communication.hw_control_communication import HWControlCommunication
from Audio.voice_record import AudioRecorder


class LaneController:
    """재활용 쓰레기 분류라인을 제어하기 위한 클래스입니다."""
    tcp_config = configparser.ConfigParser()
    gpio_config = configparser.ConfigParser()
    tcp_config.read("resources/communication_config.ini")
    gpio_config.read("resources/gpio_config.ini")

    def __init__(self):
        self.hw_ctrl_thread_running = True
        self.send_frame_thread_running = True
        self._init_comm()
        self._init_hw()
        self._init_thread()

    def __del__(self):
        self.camera.release()

    def _init_comm(self):
        self.image_comm = ImageCommunication(
            self.tcp_config["IP"]["SERVER"],
            int(self.tcp_config["PORT"]["IMAGE_PORT"])
        )

        self.audio_comm = AudioCommunication(
            self.tcp_config["IP"]["SERVER"],
            int(self.tcp_config["PORT"]["AUDIO_PORT"])
        )

        self.hw_control_comm = HWControlCommunication(
            self.tcp_config["IP"]["LANE_1"],
            int(self.tcp_config["PORT"]["STRING_PORT"])
        )

    def _init_hw(self):
        GPIO.cleanup()
        self.lane_button_controller = Button(
            int(self.gpio_config["GPIO"]["LANE_BUTTON_PIN"])
        )
        self.audio_button_controller = Button(
            int(self.gpio_config["GPIO"]["AUDIO_BUTTON_PIN"])
        )
        self.rc_servo_motor = RCServoMotor(
            int(self.gpio_config["GPIO"]["RC_SERVO_PIN1"]),
            int(self.gpio_config["GPIO"]["RC_SERVO_PIN2"])
        )
        self.servo_motor = ServoMotor(
            int(self.gpio_config["GPIO"]["SERVO_PIN"])
        )
        self.lcd_controller = LCD()
        self.recorder = AudioRecorder()
        self.camera = cv2.VideoCapture(0)

    def _init_thread(self):
        self.listen_hw_control_thread = threading.Thread(
            target=self.hw_control_comm.receive, daemon=True
        )
        self.hw_control_thread = threading.Thread(
            target=self.hw_control, daemon=True
        )
        self.webcam_thread = threading.Thread(
            target=self.send_frame_to_server, daemon=True
        )

    def hw_control(self):
        """클라이언트 라즈베리파이에 연결된 하드웨어를 제어합니다."""
        while self.hw_ctrl_thread_running:
            # 푸시버튼 제어1: Lane Start/Stop 토글
            if self.lane_button_controller.sensingBTN() is False:
                self.toggle_rc_servo_motor()

            # 푸시버튼 제어2: 5초간 음성녹음 실시후 서버로 전송
            if self.audio_button_controller.sensingBTN() is False:
                threading.Thread(
                    target=self.record_voice_and_send,
                    daemon=True
                ).start()
                time.sleep(0.5)

            # DC모터 제어1: 서버로부터 Lane Start 명령을 받아 수행
            if self.hw_control_comm.msg == "RC Start":
                self.hw_control_comm.msg = ""
                self.toggle_rc_servo_motor()
            # DC모터 제어2: 서버로부터 Lane Stop 명령을 받아 수행
            elif self.hw_control_comm.msg == "RC Stop":
                self.hw_control_comm.msg = ""
                self.toggle_rc_servo_motor()
            # 서보모터 제어: 서버로부터 받은 분류결과를 바탕으로 분류작업 실시
            elif self.hw_control_comm.msg == "Servo Kick":
                self.hw_control_comm.msg = ""
                self.servo_motor.kick()
            # 스피커 제어: 서버로부터 받은 메뉴얼 기반 text generation을 출력
            elif self.hw_control_comm.msg == "pet":
                self.lcd_controller.display_lcd("Pet")
                self.speak("페트병 분류 모델로 변경합니다.")
                self.hw_control_comm.msg = ""
            elif self.hw_control_comm.msg == "glass":
                self.lcd_controller.display_lcd("Glass")
                self.speak("유리병 분류 모델로 변경합니다.")
                self.hw_control_comm.msg = ""
            elif self.hw_control_comm.msg.startswith("@"):
                message = self.hw_control_comm.msg[1:]
                self.hw_control_comm.msg = ""
                threading.Thread(
                    target=self.speak, args=(message,),
                    daemon=True
                ).start()
            # 프로그램 종료
            elif self.hw_control_comm.msg == "/deactivate LANE_1":
                self.exit()

    def send_frame_to_server(self):
        """웹캠으로부터 얻은 이미지 프레임을 서버로 전송합니다."""
        while self.send_frame_thread_running:
            _, frame = self.camera.read()
            if frame is None:
                continue
            self.image_comm.send_frame(frame)
            time.sleep(1/30)

    def toggle_rc_servo_motor(self):
        """레인의 동작상태(start/stop)를 토글합니다."""
        if self.rc_servo_motor.running:
            self.rc_servo_motor.stop()
            self.lcd_controller.display_lcd("RCStop")
        else:
            self.rc_servo_motor.start()
            self.lcd_controller.display_lcd("RCStart")

    def record_voice_and_send(self):
        """마이크로 5초간 음성을 녹음하고 결과파일을 서버로 전송합니다."""
        self.recorder.record_and_save()
        self.audio_comm.send_audio_file(self.recorder.file_path)

    def speak(self, text):
        """서버로부터 받은 문자열을 TTS하여 스피커로 출력합니다."""
        print("받은 문자", text)
        tts = gTTS(text=text, lang="ko")
        tts.save("resources/text_to_speech.mp3")

        pygame.mixer.init()
        pygame.mixer.music.load("resources/text_to_speech.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def execute(self):
        """스레드를 실행시킵니다."""
        self.webcam_thread.start()
        self.listen_hw_control_thread.start()
        self.hw_control_thread.start()
        self.hw_control_thread.join()
        self.listen_hw_control_thread.join()
        self.webcam_thread.join()

    def exit(self):
        self.send_frame_thread_running = False
        self.hw_control_comm.running = False
        self.hw_ctrl_thread_running = False
