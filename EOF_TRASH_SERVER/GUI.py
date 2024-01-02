from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QTextEdit, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
# from io import BytesIO
import queue
from multi_thread import Rcv_webcam_Thread

    
class MainGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.frame_queue = queue.Queue()
        self.initUI()
        self.start_multi_thread()
        # Counter variable
        self.counter = 0

    def initUI(self):
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

    def start_multi_thread(self):
        #스레드 1 시작
        self.webcam_Thread = Rcv_webcam_Thread()
        self.webcam_Thread.new_frame.connect(self.update_image)
        self.webcam_Thread.start()
        

    def update_image(self, current_frame):
        # QLabel을 새 이미지로 업데이트
        pixmap = QPixmap.fromImage(current_frame)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap)
        else:
            print("Invalid image data.2")



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