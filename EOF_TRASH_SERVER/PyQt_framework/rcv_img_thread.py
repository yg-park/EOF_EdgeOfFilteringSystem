"""
ㅇ
"""
from PyQt5.QtCore import QThread
from Comm.image_comm import Image_comm


class ReceiveImage(QThread):
    """ㅇ"""
    def __init__(self, frame_queue, ip_address, port):
        super().__init__()
        self.MyReceiveImage = Image_comm(
            ip_address=ip_address,
            port=port,
            frame_queue=frame_queue
        )

    def run(self):
        self.MyReceiveImage.receive()
