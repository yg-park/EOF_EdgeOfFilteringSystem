import cv2
from datetime import datetime
import serial
import json
from os import getcwd
from os.path import join
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import client
import face_detector

# 전역 인스턴스
serialForArduino = serial.Serial('/dev/ttyACM0', 9600)
socketForRFID = client.ClientCommunication("10.10.15.58", 8888)
socketForManager = client.ClientCommunication("10.10.15.58", 8889) # 포트 다름. 8889임.


class WebcamThread(QThread):
    global socketForRFID
    change_pixmap_signal = pyqtSignal(QImage)
    update_information = pyqtSignal(str)

    def __init__(self): 
        super().__init__()
        self.manager_call_flag = False
        self.running = False # False: 웹캠 정지 상태 / True: 웹캠 동작 상태
        self.information = ""
        self.faceDetector = face_detector.FaceDetector()
        with open(join(getcwd(), "model/label_name.json"), 'r') as json_file:
            self.label_name = json.load(json_file)

    def run(self):   
        cap = cv2.VideoCapture(0)

        while self.running:
            ret, frame = cap.read()

            # 관리실 문열기 요청 버튼을 누른 순간 이미지가 한번 저장되어야 함
            if self.manager_call_flag:
                image_filename = "resources/captured_image.jpg"
                cv2.imwrite(image_filename, frame) # client.py 127번재 라인이 참조하는 실제파일 저장 타이밍
                self.manager_call_flag = False

            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                face_gray_image = self.faceDetector.get_faceROI(rgb_image)
                if face_gray_image is None:
                    display_string = "Please look at the camera"
                    cv2.putText(rgb_image,display_string,(100,80), cv2.FONT_HERSHEY_DUPLEX, 1, (250,120,255),1)
                    display_string = "for correct face recognition"
                    cv2.putText(rgb_image,display_string,(100,110), cv2.FONT_HERSHEY_DUPLEX, 1, (250,120,255),1)
                    pass
                else:
                    image_filename = "resources/face_on_captured_image.jpg"
                    cv2.imwrite(image_filename, face_gray_image)
                
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                frameQimage = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
                self.change_pixmap_signal.emit(frameQimage)

                if socketForRFID.rcvUidFromRFID_flag:
                    image_filename = "resources/captured_image.jpg"
                    cv2.imwrite(image_filename, frame) # client.py 127번재 라인이 참조하는 실제파일 저장 타이밍

                    if socketForRFID.rcvImgFromServer_flag:                    
                        captured_image_path = "resources/face_on_captured_image.jpg"
                        received_image_path = "resources/received_image.jpg"

                        captured_image_mat = cv2.cvtColor(cv2.imread(captured_image_path), cv2.COLOR_RGB2GRAY)
                        received_image_mat = cv2.cvtColor(cv2.imread(received_image_path), cv2.COLOR_RGB2GRAY)
                    
                        ci_id_, ci_conf = self.faceDetector.model.predict(captured_image_mat)
                        ri_id_, ri_conf = self.faceDetector.model.predict(received_image_mat)
                        
                        print(f"ci_id_: {ci_id_}")
                        print(f"ri_id_: {ri_id_}")
                        ri_id_confidence = int(100*(1-(ri_conf)/300))
                        ci_id_confidence = int(100*(1-(ci_conf)/300))

                        if ci_id_ == ri_id_ and \
                            ci_id_confidence > 75 and \
                                  ri_id_confidence > 75:
                            self.information = "인증완료. 입장 가능합니다."
                            self.update_information.emit(self.information)
                            print("동일인") 
                            
                            # 서보모터 문 열기
                            command = "A180\n" # ex: A180\n
                            serialForArduino.write(command.encode())

                            name = self.label_name[str(ci_id_)] #ID를 이용하여 json에서 이름 가져오기
                            socketForRFID.authentication_log = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + name + " Enter Complete!!!"
                            socketForRFID.authentication_flag = True
                            socketForRFID.manager_flag = True
                        else:
                            self.information = "인증실패! 입장 불가능합니다!"
                            self.update_information.emit(self.information)
                            print("다른 사람")

                            # 서보모터 문 닫기
                            command = "A0\n" # ex: A0\n
                            serialForArduino.write(command.encode())

                            # 경고 부저 울리기
                            command = "Z\n"
                            serialForArduino.write(command.encode())

                            socketForRFID.authentication_log = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Reject trial..."
                            socketForRFID.authentication_flag = True
                
                        socketForRFID.rcvImgFromServer_flag = False
                        socketForRFID.rcvUidFromRFID_flag = False

        cap.release() 

        # 웹캠 정지 상태에는 IDLE이미지 출력
        idle_frame = cv2.imread("resources/idle_frame.png")
        idle_frame = cv2.cvtColor(idle_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = idle_frame.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(idle_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        frameQimage = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
        self.change_pixmap_signal.emit(frameQimage)

    def resume(self):
        self.running = True

    def pause(self):
        self.running = False
    
    def manager_call(self):
        self.manager_call_flag = True


class RfidCommThread(QThread):
    global socketForRFID

    def __init__(self):
        super().__init__()

    def run(self):
        socketForRFID.communicate() # 이 함수 안에서 while 도는 중


class ManagerCommThread(QThread):
    global socketForManager
    update_information = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.request_status = 0 # 0: IDLE 상태 / 1: 관리자 요청이 발생하여 서버에 요청한 상태 / 2: 서버의 응답을 기다리는 상태
        self.information = ""

    def run(self):
        while True:
            if self.request_status == 1:
                socketForManager.send_communicate_manager()
                self.request_status = 2

            elif self.request_status == 2:
                socketForManager.receive_communicate_manager()
                if socketForManager.manager_flag == True:
                    if socketForManager.manager_responce_status == 1:
                        # 서보모터 문 열기
                        command = "A180\n" # ex: A180\n
                        serialForArduino.write(command.encode())
                        socketForManager.manager_responce_status = 0
                        # PyQt GUI 갱신하기
                        self.information = "관리자의 요청을 승인하여 문을 개방합니다!!!"
                        self.update_information.emit(self.information)

                    elif socketForManager.manager_responce_status == 2 :
                        # 서보모터 문 닫기
                        command = "A0\n" # ex: A180\n
                        serialForArduino.write(command.encode())
                        socketForManager.manager_responce_status = 0
                        # 경고 부저 울리기
                        command = "Z\n"
                        serialForArduino.write(command.encode())
                        # PyQt GUI 갱신하기
                        self.information = "관리자가 요청을 거부했습니다..."
                        self.update_information.emit(self.information)

                    else :
                        pass

                    self.request_status = 0 # 플래그 초기화
                    socketForManager.manager_flag = False # 플래그 초기화
            else:
                pass
                
    def request(self):
        self.request_status = 1


class ArduinoThread(QThread):
    global socketForRFID
    manager_call_trigger = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()

    def run(self):
        while True:    
            data = serialForArduino.readline().decode('utf-8').strip()

            # RFID 태그를 트리거로 발동하는 서버 통신에 관여하는 if문
            if data and data.startswith("U"):
                uid_ = data[1:] # 헤더 "U"를 제외한 부분이 UID
                socketForRFID.uid = uid_
                socketForRFID.arduino_rfid_flag = True

            # 관리자 호출버튼을 트리거로 발동하는 서버통신
            if data and data.startswith("T"):
                print("버튼 눌렸다")
                self.manager_call_trigger.emit(True) # True: 트리거가 발생했다 / False: IDLE상태


class App(QMainWindow):
    global arduino_manager_call_flag

    def __init__(self):
        super().__init__()

        # self.serial_port = serial_port
        self.title = "EOF NUGU:SEM - Client"
        self.top = 100
        self.left = 100
        self.width = 640
        self.height = 580

        # 4초에 한번씩 Edit Control 초기화
        self.timer = QTimer(self)
        self.timer.start(4000)
        self.timer.timeout.connect(self.refresh_lineEdit_info)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        # 웹캠 시작/정지 버튼생성
        btn_webCamStart = QPushButton("웹캠 시작")
        layout.addWidget(btn_webCamStart)
        btn_webCamStop = QPushButton("웹캠 정지")
        layout.addWidget(btn_webCamStop)

        # 웹캠 시작/정지 시그널-슬롯 연결하기
        btn_webCamStart.clicked.connect(self.resume)
        btn_webCamStop.clicked.connect(self.pause)
        
        # 웹캠 영상 출력 라벨 생성
        self.label = QLabel(self)
        layout.addWidget(self.label)

        # 웹캠 스레드 생성
        self.thread_webCam = WebcamThread()
        self.thread_webCam.change_pixmap_signal.connect(self.update_image)
        self.thread_webCam.update_information.connect(self.print_info_to_lineEdit_info) # 라인 에디트 시그널 슬롯 연결
        self.thread_webCam.start()

        # 관리실 통신 스레드 생성
        self.thread_manager_comm = ManagerCommThread()
        self.thread_manager_comm.update_information.connect(self.print_managerInfo_to_lineEdit_info)
        self.thread_manager_comm.start()

        # TCP IP 통신 스레드 생성
        self.thread_comm = RfidCommThread()
        self.thread_comm.start()

        # 아두이노 시리얼 통신 스레드 생성
        self.arduino_thread = ArduinoThread()
        self.arduino_thread.manager_call_trigger.connect(self.manager_request_arduino)
        self.arduino_thread.start()
        
        # 각종 정보 출력 라인 에디트 생성
        self.lineEdit_info = QLineEdit(self)
        self.lineEdit_info.setAlignment(Qt.AlignCenter)
        self.lineEdit_info.setReadOnly(True)
        self.lineEdit_info.setStyleSheet("background-color : gray")
        self.lineEdit_info.setPlaceholderText("여기에 각종 정보가 출력됩니다.")
        layout.addWidget(self.lineEdit_info)

        # 관리실 문 열기 요청 버튼 생성
        btn_managerRequest = QPushButton("관리실 인증 요청")
        layout.addWidget(btn_managerRequest)
        btn_managerRequest.clicked.connect(self.manager_request)


    # 웹캠 동영상 프레임 갱신 슬롯
    def update_image(self, img):
        self.label.setPixmap(QPixmap.fromImage(img))

    # 웹캠 시작버튼 시그널 대응 슬롯
    def resume(self):
        self.thread_webCam.resume()
        self.thread_webCam.start()

    # 웹캠 정지버튼 시그널 대응 슬롯
    def pause(self):
        self.thread_webCam.pause()

    # 관리실 인증 요청 PyQt GUI버튼 시그널 대응 슬롯
    def manager_request(self):
        if self.thread_webCam.running == True:
            self.thread_webCam.manager_call()
            self.thread_manager_comm.request()
            self.lineEdit_info.setStyleSheet("background-color : orange")
            self.lineEdit_info.setText("관리자 승인 대기중...")
            self.timer.stop()

    # 관리실 인증 요청 아두이노 물리버튼 시그널 대응 슬롯
    @pyqtSlot(bool)
    def manager_request_arduino(self, status):
        if status == True:
            self.manager_request()
            status = False

    # 각종 정보 출력 에디트라인 시그널 대응 슬롯
    @pyqtSlot(str)
    def print_info_to_lineEdit_info(self, information):
        if information == "인증완료. 입장 가능합니다.":
            self.lineEdit_info.setStyleSheet("background-color : green")
            self.lineEdit_info.setText(information)
            self.timer.start(4000)
        elif information == "인증실패! 입장 불가능합니다!":
            self.lineEdit_info.setStyleSheet("background-color : red")
            self.lineEdit_info.setText(information)
            self.timer.start(4000)

    # 각종 정보 출력 슬롯
    @pyqtSlot(str)
    def print_managerInfo_to_lineEdit_info(self, information):
        if information == "관리자의 요청을 승인하여 문을 개방합니다!!!":
            self.lineEdit_info.setStyleSheet("background-color : green")
            self.lineEdit_info.setText(information)
            self.timer.start(4000)
        elif information == "관리자가 요청을 거부했습니다...":
            self.lineEdit_info.setStyleSheet("background-color : red")
            self.lineEdit_info.setText(information)
            self.timer.start(4000)

    # 주기적으로 정보창 초기화
    def refresh_lineEdit_info(self):
        self.lineEdit_info.setStyleSheet("background-color : gray")
        self.lineEdit_info.setText("")
