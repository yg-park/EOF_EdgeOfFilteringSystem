import cv2
import socket
import numpy as np
import struct
from Comm.communication import Communication

class Image_comm(Communication):
    def __init__(self, ip_address, port, frame_queue) -> None:
        """ ip_address 는 서버의 ip address 입니다.
            port 번호는 socket 에 할당할 unique 한 번호로
            클라이언트와 서버가 같은 port 번호를 사용해야 합니다.
        """        
        self.ip_address = ip_address
        self.port = port
        self.frame_queue = frame_queue
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip_address, self.port))
        self.socket.listen(1)
    
    def __del__(self):
        self.socket.close()
    
    def receive(self):
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
            self.frame_queue.put(img_np)