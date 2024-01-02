import cv2
import socket
import struct

class ClientCommunication:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip_address, self.port))
        
    def __del__(self):
        # Close the client socket
        self.client_socket.close()

    def send_frame(self, frame):
        
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()
        
        # 이미지 데이터의 길이를 전송
        self.client_socket.sendall(struct.pack("!I", len(img_bytes)))

        # 이미지 데이터 전송
        self.client_socket.sendall(img_bytes)

#RTSP
#GStreamer