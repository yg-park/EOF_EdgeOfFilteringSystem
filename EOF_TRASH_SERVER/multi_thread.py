from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread, pyqtSignal
from Comm.image_comm import Image_comm
import queue

# string 출력을 통해 스레드가 잘 돌고 있다는 테스트용
class ReceiveImage(QThread):
    new_frame = pyqtSignal(QImage)
    
    def __init__(self, frame_queue):
        super().__init__()
        self.frame_queue = frame_queue
        self.MyReceiveImage = Image_comm(ip_address='10.10.15.58', port=5555, frame_queue=self.frame_queue)

    def run(self):
        self.MyReceiveImage.receive()


class Rcv_webcam_Thread(QThread):
    new_frame = pyqtSignal(QImage)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.frame_queue = queue.Queue()
        self.webcam_server_thread = ReceiveImage(self.frame_queue)

    def run(self):
        self.webcam_server_thread.start()

        while True:
            if not self.frame_queue.empty():
                image_data = self.frame_queue.get()

                # 서버에서 수신한 이미지 numpy array를 QImage로 변환
                height, width, channels = image_data.shape
                bytes_per_line = channels * width
                q_image = QImage(image_data.data, width, height, bytes_per_line, QImage.Format_BGR888)            
                
                if not q_image.isNull():
                    # 유효한 이미지인 경우에만 시그널을 발생시킴
                    self.new_frame.emit(q_image)
                else:
                    print("Invalid image data.1")