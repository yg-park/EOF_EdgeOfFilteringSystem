"""오디오 녹음을 위한 모듈입니다."""
import pyaudio
import wave

# 녹음할 시간 (초)
DURATION = 5

# 샘플 레이트와 CHUNK 크기 설정
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024


class AudioRecorder:
    """오디오 녹음을 위한 클래스입니다."""
    def __init__(self):
        self.count = -1
        self.filename = f'Audio/output_{self.count}.wav'
        
    def start_recording(self) -> str:
        """음성 메세지를 녹음하고 저장합니다."""
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("Recording...")
        
        frames = []

        # 5초 동안 녹음
        for _ in range(0, int(RATE / CHUNK * DURATION)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("Recording complete.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        self._save_to_wav(frames)
        
        return self.filename

    def _save_to_wav(self, frames):
        self.count = (self.count + 1) % 5
        self.filename = f'Audio/output_{self.count}.wav'
            
        p = pyaudio.PyAudio()

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(frames))
        wf.close()

        p.terminate()

        print(f"Audio saved to {self.filename}")
        # return self.filename
