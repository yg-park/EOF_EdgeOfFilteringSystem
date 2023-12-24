import socket
import struct
import cv2


class UDPClient:
    def __init__(self, server_ip, port):
        self.server_ip = server_ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.MAX_CHUNK_SIZE = 65507  # UDP 페이로드의 최대 크기
        self.TARGET_WIDTH = 320 # width for frame resizing
        self.TARGET_HEIGHT = 240 # height for frame resizing


    def __del__(self):
        if self.client_socket:
            self.client_socket.close()

    
    def send_webcam_frame_to_server(self, frame):
        """
        desc: 640*480 해상도의 input frame을 320*240로 resize하여 서버로 전송합니다.
        param1: 640*480 해상도의 input frame
        """
        # 예외처리
        if frame is None:
            print("error: 빈 프레임 입력")
            return
        
        # 프레임 크기 조절
        frame = cv2.resize(frame, (self.TARGET_WIDTH, self.TARGET_HEIGHT))

        # 프레임을 JPEG로 압축하여 바이트로 변환
        _, img_encoded = cv2.imencode('.jpg', frame)

        # 이미지 크기 정보를 추가하여 전송
        img_size = len(img_encoded)
        packed_size = struct.pack("!I", img_size)

        # 이미지 데이터를 청크로 분할
        img_bytes = img_encoded.tobytes()
        for i in range(0, len(img_bytes), self.MAX_CHUNK_SIZE):
            chunk = img_bytes[i:i + self.MAX_CHUNK_SIZE]

            # 각 청크에 이미지 크기 정보 추가
            img_data = packed_size + chunk

            # UDP로 프레임 청크 전송
            self.client_socket.sendto(img_data, (self.server_ip, self.port))

            # 각 청크마다 전송된 바이트 수 출력
            # print(f"전송된 바이트 수: {len(img_data)}")
