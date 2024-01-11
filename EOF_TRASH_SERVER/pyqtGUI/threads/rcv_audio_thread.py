"""
오디오 통신을 위한 스레드 모듈입니다.
"""
import time
import socket
from pathlib import Path
from PyQt5.QtCore import QThread, pyqtSignal


class ReceiveAudio(QThread):
    """오디오 통신을 위한 스레드 객체 입니다."""
    rcv_audio_signal = pyqtSignal()

    def __init__(self, ip_address, port):
        super().__init__()
        self.ip_address = ip_address
        self.port = port

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.socket.bind((self.ip_address, self.port))
        self.socket.listen(1)
        self.running = True
        print("ReceiveAudio제대로 init완료")

    def __del__(self):
        self.socket.close()
        print("ReceiveAudio소켓 반환 되었는가?")


    def run(self):
        """클라이언트 측에서 녹음한 내용을 수신합니다."""

        while self.running:
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
            self.rcv_audio_signal.emit()

    def stop(self):
        """스레드를 종료합니다."""
        self.running = False
        time.sleep(1)
        # self.socket.close()
        # self.quit()
