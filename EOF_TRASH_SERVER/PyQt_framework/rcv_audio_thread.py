"""_summary_"""
from PyQt5.QtCore import QThread
from Comm.audio_comm import AudioComm


class ReceiveAudio(QThread):
    """ㅇ"""
    def __init__(self):
        super().__init__()
        self.comm_instance = AudioComm()

    def run(self):
        self.comm_instance.receive()
