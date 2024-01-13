"""
이미지 통신을 위한 스레드 모듈입니다.
"""
import time
import socket
import struct
import cv2
import numpy as np
from PyQt5.QtCore import QThread


class ReceiveImage(QThread):
    """이미지 통신을 위한 스레드 객체입니다."""
    def __init__(self, frame_queue, ip_address, port):
        super().__init__()
        self.frame_queue = frame_queue
        self.ip_address = ip_address
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.socket.bind((self.ip_address, self.port))
        self.socket.listen(1)
        self.running = True

    def __del__(self):
        self.socket.close()

    def run(self):
        """이미지를 수신 받는 함수입니다. 수신받은 이미지를 큐에 삽입합니다."""
        print(f'Serving on {self.ip_address}:{self.port}')
        client_socket, addr = self.socket.accept()
        print(f'Connection from {addr}')

        while self.running:
            # 이미지 데이터의 길이를 수신
            img_len = struct.unpack("!I", client_socket.recv(4))[0]

            # 이미지 데이터를 수신
            img_data = b""
            while len(img_data) < img_len:
                chunk = client_socket.recv(min(img_len - len(img_data), 4096))
                if not chunk:
                    break
                img_data += chunk

            # 바이트로 된 이미지 데이터를 이미지 포맷으로 변환
            img_np = cv2.imdecode(np.frombuffer(img_data, dtype=np.uint8), 1)
            self.frame_queue.put(img_np)

    def stop(self):
        """스레드를 종료합니다."""
        self.running = False
        time.sleep(1)
        # self.quit()
        # self.socket.close()
