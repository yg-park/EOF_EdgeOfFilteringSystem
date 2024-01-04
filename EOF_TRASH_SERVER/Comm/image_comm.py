"""
이 파일은 이미지 통신을 위한 모듈 입니다.
"""
import socket
import struct
import cv2
import numpy as np

IP_ADDRESS = "10.10.15.58"
IMG_PORT = 5555


class ImageComm():
    """이미지를 통신하기 위한 클래스입니다."""
    def __init__(self):
        self.ip_address = IP_ADDRESS
        self.port = IMG_PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip_address, self.port))
        self.socket.listen(1)

    def __del__(self):
        self.socket.close()

    def receive(self, frame_queue) -> None:
        """이미지를 수신 받는 함수입니다. 수신받은 이미지를 큐에 삽입합니다.
        
        : param1(frame_queue) - 이미지를 저장할 큐 입니다.
        """
        print(f'Serving on {self.ip_address}:{self.port}')
        client_socket, addr = self.socket.accept()
        print(f'Connection from {addr}')

        while True:
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
            frame_queue.put(img_np)
