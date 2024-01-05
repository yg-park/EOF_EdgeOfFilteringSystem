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

    def send_audio_file(self, file_path):
        """오디오 파일을 송신합니다."""
        try:
            # file_path = 'audio/output.wav'
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = (self.ip_address, self.port)
            print(f"Connecting to {server_address}...")
            client_socket.connect(server_address)
            # 파일 전송
            with open(file_path, 'rb') as file:
                data = file.read(1024)
                while data:
                    client_socket.send(data)
                    data = file.read(1024)

            print("File sent successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # 소켓 닫기
            client_socket.close()
