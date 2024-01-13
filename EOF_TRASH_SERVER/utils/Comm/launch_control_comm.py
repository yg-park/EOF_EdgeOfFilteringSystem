"""
이 파일은 하드웨어 제어를 위한 통신 모듈입니다.
"""
import socket


class LaunchControlComm():
    """여러 라인의 프로그램 시작을 제어하기 위한 통신 클래스입니다."""
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        self.client_socket.close()
        print("LaunchControlComm소켓 반환 되었는가?")

    def activate(self) -> None:
        """ 하드웨어를 제어할 명령을 보냅니다."""
        message = "/activate LANE_1"

        self.client_socket.connect((self.ip_address, self.port))
        self.client_socket.sendall(message.encode('utf-8'))
        self.client_socket.close()
