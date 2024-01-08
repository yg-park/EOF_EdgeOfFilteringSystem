"""
메인 GUI 출력을 담당하는 모듈입니다.
"""
import queue
import time
import cv2
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QTextEdit, QPushButton
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import Qt, QTimer

from utils.Comm.hw_control_comm import HwControlComm
from utils.Inference.bottle_detector import BottleDetector
from utils.Inference.bottle_classifier import BottleClassifier

from pyqtGUI.threads.rcv_audio_thread import ReceiveAudio
from pyqtGUI.threads.rcv_img_thread import ReceiveImage
from pyqtGUI.threads.ROI_detect_classify_thread import ClassifyTimingChecker
from pyqtGUI.threads.audio_processing_thread import AudioProcessing


class MainGUI(QMainWindow):
    """메인 GUI에 관한 클래스입니다."""
    def __init__(self):
        super().__init__()
        self.init_UI()  # 기본 UI틀을 생성합니다.
        self.frame_queue = queue.Queue(maxsize=30)  # 동영상 스트리밍용 queue를 생성합니다.
        self.init_threads()  # 프로그램 동작에 필요한 스레드를 실행합니다.

        # 일정한 프레임으로 영상 출력을 위한 타이머를 초기화합니다.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_pixmap)
        self.timer.start(30)  # 초당 30프레임

        self.hw_control_comm = HwControlComm()
        self.detector = BottleDetector()
        self.classifier = BottleClassifier()

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

        self.log_text = QTextEdit(self)
        self.log_text.setPlainText("Log")
        self.log_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.user_input_text = QTextEdit(self)
        self.user_input_text.setPlainText("User Input")
        self.user_input_text.setMaximumHeight(30)
        self.enter_clicked_btn = QPushButton('전송')
        self.enter_clicked_btn.clicked.connect(self.enter_clicked)

        main_vertical_layout = QVBoxLayout()
        sub_horizontal_layout_1 = QHBoxLayout()
        sub_horizontal_layout_2 = QHBoxLayout()

        sub_horizontal_layout_1.addWidget(self.line_start_btn)
        sub_horizontal_layout_1.addWidget(self.line_stop_btn)

        sub_horizontal_layout_2.addWidget(self.user_input_text)
        sub_horizontal_layout_2.addWidget(self.enter_clicked_btn)

        main_vertical_layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        main_vertical_layout.addLayout(sub_horizontal_layout_1)
        main_vertical_layout.addWidget(self.log_text)
        main_vertical_layout.addLayout(sub_horizontal_layout_2)
        self.layout.addLayout(main_vertical_layout)

    def init_threads(self):
        """ 프로그램 동작에 필요한 스레드들을 실행합니다

            video_stream_thread는
            클라이언트로부터 영상을 송신받는 스레드 입니다.

            audio_recv_thread는
            클라이언트로부터 음성을 송신받는 스레드 입니다.

            ClassifyTimingCheck_thread는
            객체가 탐지되었을 때 단한번만 분류를 실시하기 위한 스레드 입니다.
        """
        self.process_client_audio_thread = AudioProcessing()
        self.process_client_audio_thread.model_change_signal.connect(
            self.change_model
        )
        # self.process_client_audio_thread.manual_tts_signal.connect()

        self.video_stream_thread = ReceiveImage(self.frame_queue)
        self.video_stream_thread.start()
        self.audio_recv_thread = ReceiveAudio()
        self.audio_recv_thread.rcv_audio_signal.connect(
            self.process_client_audio_thread.start
        )
        self.audio_recv_thread.start()

        self.ClassifyTimingCheck_thread = ClassifyTimingChecker()
        self.ClassifyTimingCheck_thread.finished_signal.connect(
            self.send_classification_result
        )

    def update_pixmap(self):
        """메인 GUI의 이미지를 업데이트 합니다."""
        if not self.frame_queue.empty():
            frame = self.frame_queue.get()

            # roi = frame[80:400, :]
            (detected, prediction_accuracy, crop_frame_coordinate) \
                = self.detector.detect_bottle(frame)

            if detected:
                cv2.rectangle(frame,
                              (crop_frame_coordinate[0], crop_frame_coordinate[1]),
                              (crop_frame_coordinate[2], crop_frame_coordinate[3]),
                              (0, 255, 0), 2)

                # 트리거
                if crop_frame_coordinate[2] > 320 and crop_frame_coordinate[2] < 480:
                    if self.ClassifyTimingCheck_thread.on_process is False:
                        self.ClassifyTimingCheck_thread.start()
                    else:
                        print("--image 들어가는중")
                        self.ClassifyTimingCheck_thread.detection_frame_list.append(
                            (prediction_accuracy,
                             frame[crop_frame_coordinate[1]:crop_frame_coordinate[3],
                                   crop_frame_coordinate[0]:crop_frame_coordinate[2]])
                        )

            height, width, channels = frame.shape
            bytes_per_line = channels * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_BGR888)

            if not q_image.isNull():
                pixmap = QPixmap.fromImage(q_image)
                self.image_label.setPixmap(pixmap)
            else:
                print("Invalid image data.1")

    def send_classification_result(self, max_accracy_frame):
        """클라이언트로 분류 결과를 전송합니다."""
        result = self.classifier.classify_bottle(max_accracy_frame)
        current_time = time.localtime()
        hour = current_time.tm_hour
        minute = current_time.tm_min
        second = current_time.tm_sec
        if result == 0:
            print("CLEAR BOTTLE 결과 전송")
            added_text = f"분류결과: 정상 {hour}시 {minute}분 {second}초"
            log = self.log_text.toPlainText() + "\n" + "사용자 입력: " + added_text
            self.log_text.setPlainText(log)
        elif result == 1:
            print("LABEL BOTTLE 결과 전송")
            self.hw_control_comm.send(message="Servo Kick")
            added_text = f"분류결과: 비정상 {hour}시 {minute}분 {second}초"
            log = self.log_text.toPlainText() + "\n" + "사용자 입력: " + added_text
            self.log_text.setPlainText(log)

    def change_model(self):
        """페트병, 유리병 모델을 스위칭 합니다."""
        current_time = time.localtime()
        hour = current_time.tm_hour
        minute = current_time.tm_min
        second = current_time.tm_sec
        if self.detector.current_target == "pet":
            self.detector.set_model_target("glass")
            added_text = f"페트병->유리병 감지. {hour}시 {minute}분 {second}초"
        elif self.detector.current_target == "glass":
            self.detector.set_model_target("pet")
            added_text = f"유리병->페트병 감지. {hour}시 {minute}분 {second}초"
        if self.classifier.current_target == "pet":
            self.classifier.set_model_target("glass")
            added_text = f"페트병->유리병 분류. {hour}시 {minute}분 {second}초"
        elif self.classifier.current_target == "glass":
            self.classifier.set_model_target("pet")
            added_text = f"유리병->페트병 분류. {hour}시 {minute}분 {second}초"
        log = self.log_text.toPlainText() + "\n" + "모델 변경: " + added_text
        self.log_text.setPlainText(log)

        print(f"현재 detector의 target = {self.detector.current_target}")
        print(f"현재 classifier target = {self.classifier.current_target}")

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
        self.hw_control_comm.send(message='RC Start')

        current_time = time.localtime()
        hour = current_time.tm_hour
        minute = current_time.tm_min
        second = current_time.tm_sec
        added_text = f"라인을 가동합니다. {hour}시 {minute}분 {second}초"
        log = self.log_text.toPlainText() + "\n" + "사용자 입력: " + added_text
        self.log_text.setPlainText(log)

    def stop_line(self):
        """라인을 중지합니다."""
        self.hw_control_comm.send(message='RC Stop')

        current_time = time.localtime()
        hour = current_time.tm_hour
        minute = current_time.tm_min
        second = current_time.tm_sec
        added_text = f"라인을 중지합니다. {hour}시 {minute}분 {second}초"
        log = self.log_text.toPlainText() + "\n" + added_text
        self.log_text.setPlainText(log)

    def enter_clicked(self):
        entered_text = self.user_input_text.toPlainText()
        log = self.log_text.toPlainText() + "\n" + "사용자 입력: " + entered_text
        self.log_text.setPlainText(log)

    def update_texts(self, text1, text2):
        pass  # No update for this example

    def closeEvent(self, event):
        """어플리케이션이 종료될 때 실행중인 스레드를 종료합니다."""
        self.video_stream_thread.quit()
        self.video_stream_thread.wait()
        self.audio_recv_thread.quit()
        self.audio_recv_thread.wait()
        event.accept()
