import socket
import struct
import time

class TCPClient:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.client_socket = None
        self.connect_to_server()


    def __del__(self):
        self.close_connection()
    

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_ip, self.port))
            print("서버에 연결되었습니다.")

        except ConnectionRefusedError:
            print("서버에 연결할 수 없습니다.")
            self.client_socket = None # 연결 실패 시 client_socket을 None으로 설정


    def close_connection(self):
        if self.client_socket:
            self.client_socket.close()


    def send_result_to_server(self, result):
        if self.client_socket:
            try:
                result_packet = struct.pack("I", result)
                self.client_socket.sendall(result_packet)
                print("데이터 전송 성공")
            except (socket.error, BrokenPipeError):
                print("데이터 전송 중 오류 발생. 재연결 시도 중...")
                self.close_connection()
                self.connect_to_server()
        else:
            print("클라이언트 소켓이 초기화되지 않았습니다. 연결이 실패했을 수 있습니다.")
