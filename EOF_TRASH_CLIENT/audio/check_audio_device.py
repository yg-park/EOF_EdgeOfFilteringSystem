import pyaudio

audio = pyaudio.PyAudio()

for index in range(audio.get_device_count()):
    desc = audio.get_device_info_by_index(index)
    print("DEVICE: {device}, INDEX: {index}, RATE: {rate} ".format(
        device=desc["name"], index=index, rate=int(desc["defaultSampleRate"])))
