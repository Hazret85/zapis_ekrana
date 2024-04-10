import numpy as np
import cv2
from PIL import ImageGrab
import pyaudio
import wave
import threading
import os


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

CHUNK = 1024
AUDIO_FILE = "output_audio.wav"
VIDEO_FILE = "output_video.avi"
SCREEN_SIZE = (1920, 1080)
audio = pyaudio.PyAudio()


def record_audio():
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    while not audio_thread_stop_event.is_set():
        data = stream.read(CHUNK)
        frames.append(data)


    stream.stop_stream()
    stream.close()


    waveFile = wave.open(AUDIO_FILE, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b"".join(frames))
    waveFile.close()


audio_thread_stop_event = threading.Event()
audio_thread = threading.Thread(target=record_audio)
audio_thread.start()


fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(VIDEO_FILE, fourcc, 13.6, (SCREEN_SIZE))

try:
    while True:
        img = ImageGrab.grab(bbox=(0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))
        img_np = np.array(img)
        out.write(cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB))

except KeyboardInterrupt:
    audio_thread_stop_event.set()
    audio_thread.join()

    out.release()
    cv2.destroyAllWindows()
    audio.terminate()


print("Запись закончена")

from moviepy.editor import *

video = VideoFileClip("output_video.avi")
audio = AudioFileClip("output_audio.wav")

combined_clip = video.set_audio(audio)
combined_clip.write_videofile("output_combined.mp4")
