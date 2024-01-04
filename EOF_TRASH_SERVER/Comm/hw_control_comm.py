"""
이 파일은 하드웨어 제어를 위한 통신 모듈입니다.
"""
import socket

IP_ADDRESS = "10.10.15.200"
STRING_SEND_PORT = 6666


class HwControlComm():
    """하드웨어를 제어하기 위한 통신 클래스입니다."""
    def __init__(self):
        self.ip_address = IP_ADDRESS
        self.port = STRING_SEND_PORT
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip_address, self.port))

    def __del__(self):
        self.client_socket.close()

    def send(self, order) -> None:
        """ 하드웨어를 제어할 명령을 보냅니다.
        
        :param1(order) - 하드웨어로 보낼 명령입니다.
        """
        self.client_socket.sendall(order.encode('utf-8'))
