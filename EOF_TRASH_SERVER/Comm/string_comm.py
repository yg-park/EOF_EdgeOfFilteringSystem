"""_summary_"""
import socket

IP_ADDRESS = "10.10.15.200"
STRING_SEND_PORT = 6666

class StringComm():
    """_summary_

    Args:
        Communication (_type_): _description_
    """
    def __init__(self):
        self.ip_address = IP_ADDRESS
        self.port = STRING_SEND_PORT       

    def receive(self):
        """_summary_
        """
        # TODO: 문자열을 수신 
        # return 문자열

    def send(self, message='2'):
        """_summary_

        Args:
            ip_address (_type_): _description_
            port (_type_): _description_
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip_address, self.port))
        self.message = message
        self.client_socket.send(self.message.encode('utf-8'))
        print(f"클라이언트에서 서버로 메시지 전송: {self.message}")
        self.client_socket.close()
