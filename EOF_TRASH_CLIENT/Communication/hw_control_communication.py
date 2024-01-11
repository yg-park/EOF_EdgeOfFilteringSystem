"""
하드웨어를 제어하는 통신을 담당하는 모듈입니다.
"""
import time
import socket


class HWControlCommunication:
    """하드웨어 제어를 위한 통신 클래스입니다."""
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.socket.bind((self.ip_address, self.port))
        self.socket.listen(1)
        self.msg = ""
        self.running = True

    def __del__(self):
        self.socket.close()

    def receive(self) -> None:
        """서버로부터 하드웨어를 제어하는 명령을 수신합니다."""
        while self.running:
            print("하드웨어 제어를 기다리고 있습니다...")
            server_socket, _ = self.socket.accept()
            print(f"서버와 연결됨: {server_socket}")
            self.msg = server_socket.recv(1024).decode('utf-8')
            print("서버로부터 받은 메시지: ", self.msg)
            time.sleep(0.1)
