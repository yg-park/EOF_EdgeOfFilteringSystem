"""
음성 메세지의 추론 결과를 통신하는 모듈입니다.
"""
import socket

IP_ADDRESS = "10.10.15.58"
VOICE_INF_PORT = 8888


class VoiceInfComm():
    """음성 메세지의 추론 결과를 통신하는 클래스입니다."""
    def __init__(self):
        self.ip_address = IP_ADDRESS
        self.port = VOICE_INF_PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip_address, self.port))

    def __del__(self):
        self.socket.close()

    def send(self, inf_result) -> None:
        """추론 결과를 전송하는 함수입니다.

        :param1(inf_result) - 음성 메세지에 대한 추론 결과입니다.
        """
