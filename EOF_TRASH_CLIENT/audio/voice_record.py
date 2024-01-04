import pyaudio
import wave
import time

class AudioRecorder:
    def __init__(self, filename='audio/output.wav', duration=5):
        self.filename = filename
        self.duration = duration
        self.frames = []
        self.is_recording = False

    def start_recording(self):
        self.is_recording = True
        self.frames = []

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)

        print("Recording...")

        start_time = time.time()

        while self.is_recording:
            audio_data = stream.read(1024)
            self.frames.append(audio_data)

            if time.time() - start_time > self.duration:
                break

        print("Recording complete.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        self.save_to_wav()

    def stop_recording(self):
        self.is_recording = False

    def save_to_wav(self):
        p = pyaudio.PyAudio()

        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()

        p.terminate()

        print(f"Audio saved to {self.filename}")


