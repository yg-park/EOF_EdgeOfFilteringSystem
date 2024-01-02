"""
ㅇ
"""
import socket


class Communication:
    """desc:

    """
    IP_ADDRESS = "10.10.15.58"

    def __init__(self, port) -> None:
        self.server_ip = self.IP_ADDRESS
        self.port = port
        self.port_image = port["PORT_IMAGE"]
        self.port_str = port["PORT_STR"]
        self.port_voice = port["PORT_VOICE"]

        self.image_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.string_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.voice_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_image_to_server(self, frame):
        """desc:

        """
        # TODO: frame을 서버로 송신합니다.

    def send_string_to_server(self, string):
        """desc:

        """
        # TODO: 추론 결과를 서버로 송신합니다.

    def send_voice_to_server(self, audio_file_path):
        """desc:

        """
        # TODO: 녹음파일을 서버로 송신합니다.

    def recv_string_from_server(self):
        """desc:

        """
        # TODO: 서버로부터 강제 동작 명령 스트링 데이터를 수신합니다.
