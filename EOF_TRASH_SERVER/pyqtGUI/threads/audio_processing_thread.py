"""
ㅇ
"""
from PyQt5.QtCore import QThread, pyqtSignal
import whisper


class AudioProcessing(QThread):
    """ㅇ"""
    model_change_signal = pyqtSignal()
    manual_tts_signal = pyqtSignal()

    AUDIO_FILE_PATH = "resources/received_audio.wav"
    model_change_keywords = ["모델", "바꿔줘"]

    def __init__(self):
        super().__init__()
        self.model = whisper.load_model("base")

    def run(self):
        """ㅇ"""
        stt = self.model.transcribe(self.AUDIO_FILE_PATH, language="ko")

        print(stt["text"])
        print(stt["language"])

        model_change_flag = False
        for keyword in self.model_change_keywords:
            if stt["text"].find(keyword) != -1:
                model_change_flag = True

        if model_change_flag:
            self.model_change_signal.emit()
