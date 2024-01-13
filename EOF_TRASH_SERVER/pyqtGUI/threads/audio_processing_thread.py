"""
오디오 파일을 전처리 하는 모듈입니다.
"""
from PyQt5.QtCore import QThread, pyqtSignal


class AudioProcessing(QThread):
    """클라이언트로부터 수신한 오디오파일을 가지고, 서버가 실행 가능한 동작을 정의한 클래스입니다."""
    model_change_signal = pyqtSignal()
    message_signal = pyqtSignal(str)

    AUDIO_FILE_PATH = "resources/received_audio.wav"
    model_change_keywords = ["change", "model"]

    def __init__(self, voice_inferencer):
        super().__init__()
        self.voice_inferencer = voice_inferencer

    def run(self):
        """resources/received_audio.wav 파일의 내용을 바탕으로 동작을 결정합니다."""
        stt = self.voice_inferencer.get_stt(self.AUDIO_FILE_PATH)
        print(stt)

        cnt = 0
        for keyword in self.model_change_keywords:
            if stt.find(keyword) != -1:
                cnt += 1

        model_change_flag = True if cnt == \
            len(self.model_change_keywords) else False

        if model_change_flag:
            self.model_change_signal.emit()
        else:
            answer = self.voice_inferencer.get_llama2_answer(stt)
            self.message_signal.emit(answer)


class TextProcessing(QThread):
    """whisper가 생성한 텍스트를 가지고 llama2 모델에 추론합니다."""
    finished_signal = pyqtSignal(str)

    def __init__(self, voice_inferencer):
        super().__init__()
        self.voice_inferencer = voice_inferencer
        self.target_text = None

    def run(self):
        """whisper가 생성한 텍스트를 가지고 llama2 모델에 추론합니다."""
        answer = self.voice_inferencer.get_llama2_answer(self.target_text)
        self.finished_signal.emit(answer)
