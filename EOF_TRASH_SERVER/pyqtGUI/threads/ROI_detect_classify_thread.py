"""
하나의 물체에 대하여 한번의 classification을 수행하기 위해 준비한 모듈입니다.
"""
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal


class ClassifyTimingChecker(QThread):
    """하나의 물체에 대하여 한번의 classification을 수행하기 위해 필요한 스레드입니다."""
    finished_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.detection_frame_list = []
        self.on_process = False

    def run(self):
        """2초동안 대기하며 MainGUI 객체가 넣어주는 프레임을 받고,
        그것을 바탕으로 가장 accuracy가 높은 프레임을 뽑아 시그널을 보냅니다.
        """
        self.on_process = True
        self.msleep(2000)  # 2초 동안 스레드 멈추고 MainGUI 객체로부터 프레임을 받음

        (_, cropped_frame) = max(self.detection_frame_list, key=lambda x: x[0])
        self.detection_frame_list.clear()
        self.on_process = False

        self.msleep(2500)
        self.finished_signal.emit(cropped_frame)
