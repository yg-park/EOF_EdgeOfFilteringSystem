"""
"""
import queue
import time
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QTextEdit, QPushButton
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt, QTimer
from PyQt_framework.rcv_img_thread import ReceiveImage
from PyQt_framework.rcv_audio_thread import ReceiveAudio
from EOF_TRASH_SERVER.Comm.hw_control_comm import HwControlComm


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

    def init_UI(self):
        """기본 UI틀을 생성합니다."""
        self.setWindowTitle("EOF Trash - Server")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.image_label = QLabel(self)
        pixmap = QPixmap("example.jpg")
        self.image_label.setPixmap(pixmap.scaled(640, 480, aspectRatioMode=Qt.KeepAspectRatio))

        self.small_text_label = QLabel("Small Centered Text", self)
        self.small_text_label.setFont(QFont("Arial", 12))

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText("Log")

        self.user_input_text_edit = QTextEdit(self)
        self.user_input_text_edit.setPlainText("User Input")

        self.button1 = QPushButton('라인 시작')
        self.button1.clicked.connect(self.operate_line)  # Connect the button's clicked signal to the method

        self.button2 = QPushButton('라인 정지')
        self.button2.clicked.connect(self.stop_line)  # Connect the button's clicked signal to the method

        main_vertical_layout = QVBoxLayout()
        sub_horizontal_layout = QHBoxLayout()
        sub_vertical_layout = QVBoxLayout()
        hor_sub_vertical_layout = QVBoxLayout()

        sub_vertical_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        sub_vertical_layout.addWidget(self.small_text_label, alignment=Qt.AlignCenter)

        hor_sub_vertical_layout.addWidget(self.user_input_text_edit)
        hor_sub_vertical_layout.addWidget(self.button1)
        hor_sub_vertical_layout.addWidget(self.button2)

        sub_horizontal_layout.addLayout(sub_vertical_layout)
        sub_horizontal_layout.addLayout(hor_sub_vertical_layout)
        main_vertical_layout.addLayout(sub_horizontal_layout)
        main_vertical_layout.addWidget(self.text_edit)

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
        self.HW_control_comm.send(message='RC operate')
        
        current_time = time.localtime()

        hour = current_time.tm_hour
        minute = current_time.tm_min
        second = current_time.tm_sec
        
        self.user_input_text_edit.setPlainText(f"라인을 가동합니다. {hour}시 {minute}분 {second}초")

    def stop_line(self):
        """라인을 중지합니다."""
        self.HW_control_comm.send(message='RC stop')
        
        current_time = time.localtime()

        hour = current_time.tm_hour
        minute = current_time.tm_min
        second = current_time.tm_sec
        
        self.user_input_text_edit.setPlainText(f"라인을 가동합니다. {hour}시 {minute}분 {second}초")

    def update_texts(self, text1, text2):
        pass  # No update for this example

    def closeEvent(self, event):
        # 어플리케이션이 종료될 때 스레드를 정리
        self.video_stream_thread.quit()
        self.video_stream_thread.wait()
        self.audio_recv_thread.quit()
        self.audio_recv_thread.wait()
        event.accept()
