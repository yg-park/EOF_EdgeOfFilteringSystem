"""
영상을 통신하기 위한 모듈입니다.
"""
import cv2
import socket
import struct


class ImageCommunication:
    """영상을 통신하기 위한 클래스입니다."""
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip_address, self.port))

    def __del__(self):
        self.client_socket.close()

    def send_frame(self, frame) -> None:
        """ 이미지를 전송합니다.
            frame: 웹캠으로부터 얻어 온 frame 입니다.
        """
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()

        # 이미지 데이터의 길이를 전송
        self.client_socket.sendall(struct.pack("!I", len(img_bytes)))

        # 이미지 데이터 전송
        self.client_socket.sendall(img_bytes)
