"""
d
"""
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal


class ClassifyTimingChecker(QThread):
    finished_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.detection_frame_list = []
        self.on_process = False

    def run(self):
        print("Thread started")
        self.on_process = True

        self.msleep(3000)  # 3초 동안 스레드 멈추고 MainGUI 객체로부터 프레임을 받음

        (_, cropped_frame) = max(self.detection_frame_list, key=lambda x: x[0])
        self.finished_signal.emit(cropped_frame)
        self.detection_frame_list.clear()
        self.on_process = False
        print("Thread finished")

