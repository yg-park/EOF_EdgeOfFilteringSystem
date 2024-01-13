"""
이 파일은 하드웨어 제어를 위한 통신 모듈입니다.
"""
import socket


class HwControlComm():
    """하드웨어를 제어하기 위한 통신 클래스입니다."""
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        print("HwControlComm 제대로 init완료")

    def send(self, message) -> None:
        """ 하드웨어를 제어할 명령을 보냅니다.

        :param1(message) - 하드웨어로 보낼 명령입니다.
        """
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.ip_address, self.port))
        client_socket.sendall(message.encode('utf-8'))
        client_socket.close()
