""" 오디오 통신을 위한 스레드 모듈입니다.
"""
from PyQt5.QtCore import QThread
from Comm.audio_comm import AudioComm


class ReceiveAudio(QThread):
    """오디오 통신을 위한 스레드 객체 입니다."""
    def __init__(self):
        super().__init__()
        self.audio_comm_instance = AudioComm()

    def run(self):
        """생성한 통신 객체를 통해 데이터를 수신합니다."""
        self.audio_comm_instance.receive()