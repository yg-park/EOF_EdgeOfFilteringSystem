"""
오디오 녹음을 위한 모듈입니다.
"""
import pyaudio
import wave

# 샘플 레이트와 CHUNK 크기 설정
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
DURATION = 5  # 녹음할 시간 (초)


class AudioRecorder:
    """오디오 녹음을 위한 클래스입니다."""
    def __init__(self):
        self.file_path = "resources/recorded_voice.wav"

    def record_and_save(self):
        """음성 메세지를 녹음하고 저장합니다."""
        print("Recording...")
        pa = pyaudio.PyAudio()

        stream = pa.open(format=FORMAT,
                         channels=CHANNELS,
                         rate=RATE,
                         input=True,
                         frames_per_buffer=CHUNK)
        # 5초 동안 녹음
        frames = []
        for _ in range(0, int(RATE / CHUNK * DURATION)):
            data = stream.read(CHUNK)
            frames.append(data)
        stream.stop_stream()
        stream.close()

        wf = wave.open(self.file_path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()

        pa.terminate()
        print("Recording complete.")
