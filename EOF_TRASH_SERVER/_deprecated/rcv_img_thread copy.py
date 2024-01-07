"""
이미지 통신을 위한 스레드 모듈입니다.
"""
from PyQt5.QtCore import QThread
from _deprecated.image_comm import ImageComm


class ReceiveImage(QThread):
    """이미지 통신을 위한 스레드 객체입니다."""
    def __init__(self, frame_queue):
        super().__init__()

        self.img_comm_instance = ImageComm()
        self.frame_queue = frame_queue

    def run(self):
        """생성한 통신 객체를 통해 데이터를 수신합니다."""
        self.img_comm_instance.receive(self.frame_queue)
