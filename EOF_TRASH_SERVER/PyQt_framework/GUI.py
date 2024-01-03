"""
ㅇ
"""
import queue
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QTextEdit, QPushButton
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt, QTimer
from PyQt_framework.rcv_img_thread import ReceiveImage


class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()  # 기본 UI틀을 생성합니다.
        self.frame_queue = queue.Queue()  # 동영상 스트리밍용 queue를 생성합니다.
        self.start_threads()  # 프로그램 동작에 필요한 스레드를 실행합니다.
        
        # 일정한 프레임으로 영상 출력을 위한 타이머를 초기화합니다.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pixmap)
        self.timer.start(30)  # 초당 30프레임
        
        # Counter variable
        self.counter = 0

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

        self.button1 = QPushButton('Button 1')
        self.button1.clicked.connect(self.button1_clicked)  # Connect the button's clicked signal to the method

        self.button2 = QPushButton('Button 2')
        self.button2.clicked.connect(self.button2_clicked)  # Connect the button's clicked signal to the method
        
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
        """프로그램 동작에 필요한 스레드들을 실행합니다"""
        # 클라이언트로부터 영상을 송신받는 스레드
        self.video_stream_thread = ReceiveImage(self.frame_queue)
        self.video_stream_thread.start()
        
    def update_pixmap(self):
        """"""
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
        main_layout = self.layout.itemAt(0)
        if main_layout:
            sub_layout = main_layout.itemAt(0)
            if sub_layout:
                text_edit_item = sub_layout.itemAt(1)
                if text_edit_item and text_edit_item.widget():
                    text_edit_item.widget().append(message)

    def button1_clicked(self):
        # Update UI when Button 1 is clicked
        self.counter += 1
        self.user_input_text_edit.setPlainText(f"Button 1 pressed, Counter: {self.counter}")
    
    def button2_clicked(self):
        # Update UI when Button 1 is clicked
        self.counter += 1
        self.user_input_text_edit.setPlainText(f"Button 2 pressed, Counter: {self.counter}")

    def update_texts(self, text1, text2):
        pass  # No update for this example

    def closeEvent(self, event):
        # 어플리케이션이 종료될 때 스레드를 정리
        self.webcam_Thread.quit()
        self.webcam_Thread.wait()
        event.accept()
