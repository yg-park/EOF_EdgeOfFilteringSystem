"""_summary_"""
import socket

IP_ADDRESS = "10.10.15.58"
AUDIO_PORT = 7777


class AudioComm():
    """_summary_
    Args:
        Communication (_type_): _description_
    """
    def __init__(self) -> None:
        self.ip_address = IP_ADDRESS
        self.port = AUDIO_PORT
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip_address, self.port))
        self.socket.listen(1)
    
    def __del__(self):
        self.socket.close()
    
    def receive(self):
        """_summary_
        """
        # return voice_file_path
        print("Waiting for a connection...")
        client_socket, client_address = self.socket.accept()
        print(f"Connection from {client_address}")

        # 파일 수신
        with open('resources/received_audio.wav', 'wb') as file:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                file.write(data)
        print("File received successfully.")