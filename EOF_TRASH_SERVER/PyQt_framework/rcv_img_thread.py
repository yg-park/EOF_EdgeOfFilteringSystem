"""
ㅇ
"""
from PyQt5.QtCore import QThread
from Comm.image_comm import Image_comm


class ReceiveImage(QThread):
    """ㅇ"""
    def __init__(self, frame_queue):
        super().__init__()
        self.MyReceiveImage = Image_comm()
        self.frame_queue = frame_queue

    def run(self):
        self.MyReceiveImage.receive(self.frame_queue)
