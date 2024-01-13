"""
프로그램 실행 명령어 통신을 담당하는 모듈입니다.
"""
import socket
import subprocess
import time

IP_ADDRESS = "10.10.15.200"
PORT = 9999


class LaunchControlCommunication:
    """하드웨어 제어를 위한 통신 클래스입니다."""
    def __init__(self):
        self.ip_address = IP_ADDRESS
        self.port = PORT
        self.msg = ""

    def __del__(self):
        self.socket.close()

    def receive(self) -> None:
        """서버로부터 하드웨어를 제어하는 명령을 수신합니다."""
        time.sleep(3)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip_address, self.port))
        self.socket.listen(1)

        while True:
            print("listen 시작")
            server_socket, _ = self.socket.accept()
            print(f"서버와 연결됨: {server_socket}")
            self.msg = server_socket.recv(1024).decode('utf-8')
            print("서버로부터 받은 메시지: ", self.msg)
            if self.msg == "/activate LANE_1":
                subprocess.run(["/bin/bash", "/home/eof/EOF_SeparateTrashCollection/EOF_TRASH_CLIENT/launch_main.sh"])


if __name__ == "__main__":
    comm = LaunchControlCommunication()
    comm.receive()
