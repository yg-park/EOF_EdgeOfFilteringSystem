from communication import Communication

class Image_comm(Communication):
    def __init__(self) -> None:
        # TODO: 이미지 통신과 관련된 포트 설정
        # TODO: 소켓 생성 및 초기화
    
    def receive(self):
        # TODO: 이미지를 수신 및 저장(?)
        
        # return 이미지 파일 패스
        
    def __store_image(self, data):
        # TODO: data 를 jpg 포맷으로 변환 후 저장
        
        # 최대 100 장 까지만 저장될 수 있도록 한다.
        # filename_000.jpg 형태로 저장 후
        # filename_100.jpg 파일이 만들어지면
        # 다시 filename_000.jpg 로 저장되도록
        # count 변수(파일 이름의 숫자 부분)를
        # circular 하게 조절한다.
        
        # return True if file is stored else False