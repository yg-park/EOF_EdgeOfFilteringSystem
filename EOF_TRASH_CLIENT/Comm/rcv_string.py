"""
ㅇ
"""
import socket

IP_ADDRESS = "10.10.15.200"
PORT = 6666


class StringComm:
    """
    desc:
    """
    def __init__(self) -> None:
        """
        desc:
        """
        self.ip_address = IP_ADDRESS
        self.port = PORT
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip_address, self.port))
        self.server_socket.listen(1)
        self.msg = 0
        print("서버가 시작되었습니다. 클라이언트를 기다리는 중...")
    
    def __del__(self) -> None:
        """
        desc:
        """
        self.server_socket.close()

    def receive(self):
        """
        desc:
        """
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"클라이언트와 연결됨: {client_address}")
            data = client_socket.recv(1024).decode('utf-8')
            if data == '1':
                response = "서버에서 1을 수신했습니다."
                self.msg = 1
            elif data == '2':
                response = "서버에서 2를 수신했습니다."
                self.msg = 2
            elif data == '3':
                response = "서버에서 3을 수신했습니다."
                self.msg = 3
            print(response)
