"""
이 파일은 오디오 파일 통신을 위한 모듈입니다.
"""
import socket
from pathlib import Path

IP_ADDRESS = "10.10.15.58"
AUDIO_PORT = 7777


class AudioComm():
    """오디오 파일을 통신하는 클래스입니다."""
    def __init__(self):
        self.ip_address = IP_ADDRESS
        self.port = AUDIO_PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip_address, self.port))
        self.socket.listen(1)

    def __del__(self):
        self.socket.close()

    def receive(self) -> None:
        """클라이언트 측에서 녹음한 내용을 수신합니다."""
        print("Waiting for a voice_receive_connection...")
        client_socket, client_address = self.socket.accept()
        print(f"Connection from {client_address}")

        file_path = Path('resources/received_audio.wav')

        # 오디오 파일 수신
        with open(file_path, 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        print("File received successfully.")
