"""
ㅇ
"""
import socket


class AudioCommunication:
    """
    desc:
    """
    def __init__(self, ip_address, port):
        """
        desc:
        """
        self.ip_address = ip_address
        self.port = port

    def send_audio_file(self):
        """
        desc:
        """
        try:
            file_path = 'audio/output.wav'
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

