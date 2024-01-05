"""
"""
import queue
import time
import cv2
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QTextEdit, QPushButton
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt, QTimer
from PyQt_framework.rcv_img_thread import ReceiveImage
from PyQt_framework.rcv_audio_thread import ReceiveAudio
from Comm.hw_control_comm import HwControlComm

from Inference.pet_bottle_detector import PetBottleDetector
from Inference.pet_bottle_classifier import PetBottleClassifier




class MainGUI(QMainWindow):
    """메인 GUI에 관한 클래스입니다."""
    def __init__(self):
        super().__init__()
        self.init_UI()  # 기본 UI틀을 생성합니다.
        self.frame_queue = queue.Queue()  # 동영상 스트리밍용 queue를 생성합니다.
        self.start_threads()  # 프로그램 동작에 필요한 스레드를 실행합니다.

        # 일정한 프레임으로 영상 출력을 위한 타이머를 초기화합니다.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pixmap)
        self.timer.start(60)  # 초당 60프레임

        self.HW_control_comm = HwControlComm()
        
        self.pet_detector = PetBottleDetector()
        self.pet_classifier = PetBottleClassifier()

        # Counter variable
        self.counter = 0

    def init_UI(self):
        """기본 UI틀을 생성합니다."""
        self.setWindowTitle("EOF Trash - Server")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.image_label = QLabel(self)
        pixmap = QPixmap("resources/idle_frame.png")
        self.image_label.setPixmap(pixmap.scaled(640, 480, aspectRatioMode=Qt.KeepAspectRatio))

        self.line_start_btn = QPushButton('라인 시작')
        self.line_start_btn.clicked.connect(self.operate_line)

        self.line_stop_btn = QPushButton('라인 정지')
        self.line_stop_btn.clicked.connect(self.stop_line)

        self.user_input_text_edit = QTextEdit(self)
        self.user_input_text_edit.setPlainText("Log")
        self.user_input_text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.user_input = QTextEdit(self)
        self.user_input.setPlainText("User Input")
        self.user_input.setMaximumHeight(30)
        self.enter_clicked_btn = QPushButton('전송')
        self.enter_clicked_btn.clicked.connect(self.enter_clicked)

        main_vertical_layout = QVBoxLayout()
        sub_horizontal_layout_1 = QHBoxLayout()
        sub_horizontal_layout_2 = QHBoxLayout()

        sub_horizontal_layout_1.addWidget(self.line_start_btn)
        sub_horizontal_layout_1.addWidget(self.line_stop_btn)

        sub_horizontal_layout_2.addWidget(self.user_input)
        sub_horizontal_layout_2.addWidget(self.enter_clicked_btn)

        main_vertical_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        main_vertical_layout.addLayout(sub_horizontal_layout_1)
        main_vertical_layout.addWidget(self.user_input_text_edit)
        main_vertical_layout.addLayout(sub_horizontal_layout_2)
        self.layout.addLayout(main_vertical_layout)

    def start_threads(self):
        """ 프로그램 동작에 필요한 스레드들을 실행합니다
        
            video_stream_thread는
            클라이언트로부터 영상을 송신받는 스레드 입니다.
            
            audio_recv_thread는
            클라이언트로부터 음성을 송신받는 스레드 입니다.
        """
        self.video_stream_thread = ReceiveImage(self.frame_queue)
        self.video_stream_thread.start()
        self.audio_recv_thread = ReceiveAudio()
        self.audio_recv_thread.start()

    def update_pixmap(self):
        """메인 GUI의 이미지를 업데이트 합니다."""
        if not self.frame_queue.empty():
            image_data = self.frame_queue.get()

            detection, center, coordinate = self.pet_detector.detect_pet_bottle(image_data)
            if detection == True:
                if center == True:
                    print("센터 잡았다")
                    # 여기서 classification을 발생시키고 클라이언트에 전송하는 로직이 추가되어야 함
                    target_crop_frame = image_data[coordinate[1]:coordinate[3],
                                                   coordinate[0]:coordinate[2]]
                    result = self.pet_classifier.classify_pet_bottle(target_crop_frame)

                    if result == 0:
                        print("추론결과 clear_bottle")
                    elif result == 1:
                        print("추론결과 label_bottle")
                        # 여기서 client가 kick을 하도록 메세지를 전송해야함

                cv2.rectangle(image_data,
                            (coordinate[0], coordinate[1]),
                            (coordinate[2], coordinate[3]),
                            (0, 255, 0), 2)

            # 여기서 조건에 따라 페트병 전처리 함수 혹은 유리병 전처리 함수를 받아야 함

            # 서버에서 수신한 이미지 numpy array를 QImage로 변환
            height, width, channels = image_data.shape
            bytes_per_line = channels * width
            q_image = QImage(image_data.data, width, height, bytes_per_line, QImage.Format_BGR888)

            if not q_image.isNull():
                pixmap = QPixmap.fromImage(q_image)
                self.image_label.setPixmap(pixmap)
            else:
                print("Invalid image data.1")



    def update_text_edit(self, message):
        """메인 GUI의 텍스트박스를 업데이트 합니다."""
        main_layout = self.layout.itemAt(0)
        if main_layout:
            sub_layout = main_layout.itemAt(0)
            if sub_layout:
                text_edit_item = sub_layout.itemAt(1)
                if text_edit_item and text_edit_item.widget():
                    text_edit_item.widget().append(message)

    def operate_line(self):
        """라인을 가동합니다."""
        self.HW_control_comm.send(message='RC Start')
        
        current_time = time.localtime()

        hour = current_time.tm_hour
        minute = current_time.tm_min
        second = current_time.tm_sec
        
        self.user_input_text_edit.setPlainText(f"라인을 가동합니다. {hour}시 {minute}분 {second}초")

    def stop_line(self):
        """라인을 중지합니다."""
        self.HW_control_comm.send(message='RC Stop')
        
        current_time = time.localtime()

        hour = current_time.tm_hour
        minute = current_time.tm_min
        second = current_time.tm_sec
        
        self.user_input_text_edit.setPlainText(f"라인을 가동합니다. {hour}시 {minute}분 {second}초")

    def enter_clicked(self):
        entered_text = self.user_input.toPlainText()
        current_text = self.user_input_text_edit.toPlainText()
        self.user_input_text_edit.setPlainText(current_text + "\n" + "사용자 입력: " + entered_text)


    def update_texts(self, text1, text2):
        pass  # No update for this example

    def closeEvent(self, event):
        # 어플리케이션이 종료될 때 스레드를 정리
        self.video_stream_thread.quit()
        self.video_stream_thread.wait()
        self.audio_recv_thread.quit()
        self.audio_recv_thread.wait()
        event.accept()
