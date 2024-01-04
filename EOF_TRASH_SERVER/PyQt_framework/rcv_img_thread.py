"""
ㅇ
"""
from PyQt5.QtCore import QThread
from Comm.image_comm import ImageComm


class ReceiveImage(QThread):
    """ㅇ"""
    def __init__(self, frame_queue):
        super().__init__()

        self.comm_instance = ImageComm()
        self.frame_queue = frame_queue

    def run(self):
        self.comm_instance.receive(self.frame_queue)

