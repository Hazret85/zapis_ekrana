from moviepy.editor import *

# Загрузка видео и аудио файлов
video = VideoFileClip("output_video.avi")
audio = AudioFileClip("output_audio.wav")

# Объединение видео и аудио
combined_clip = video.set_audio(audio)

# Сохранение объединенного файла
combined_clip.write_videofile("output_combined.mp4")

