"""
오디오 통신을 위한 모듈입니다.
"""
import socket

IP_ADDRESS = "10.10.15.58"
PORT = 7777


class AudioCommunication:
    """오디오 파일을 통신하기 위한 클래스입니다."""
    def __init__(self):
        self.ip_address = IP_ADDRESS
        self.port = PORT

    def __del__(self):
        self.client_socket.close()

    def send_audio_file(self, file_path):
        """오디오 파일을 송신합니다."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.ip_address, self.port)
        print(f"Connecting to {server_address}...")
        self.client_socket.connect((self.ip_address, self.port))

        with open(file_path, 'rb') as file:
            data = file.read(1024)
            while data:
                self.client_socket.send(data)
                data = file.read(1024)
        self.client_socket.close()
        print("File sent successfully.")
