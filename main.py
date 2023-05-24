from pydub import AudioSegment
import scipy
import numpy as np
import matplotlib.pyplot as plt

from filters import AudioFile

file = AudioFile("audio_files/test_audio/RockAndRoll.wav", "audio_files/test_audio/RockAndRoll_bad.wav")
file.exponentional_filter()
file.plotter(channel=0, left=0, right=1, title="", xlabel="Время (в 1 / rate секундах)", ylabel="Амплитуда")
file.plotter(channel=0, left=0, right=1, title="", xlabel="Частота", ylabel="Амплитуда", is_spec=True)

file = AudioFile("audio_files/test_audio/RockAndRoll.wav", "audio_files/test_audio/RockAndRoll_bad.wav")
file.spectral_subtraction_filter()
file.plotter(channel=0, left=0, right=1, title="", xlabel="Время (в 1 / rate секундах)", ylabel="Амплитуда")
file.plotter(channel=0, left=0, right=1, title="", xlabel="Частота", ylabel="Амплитуда", is_spec=True)

file = AudioFile("audio_files/test_audio/RockAndRoll.wav", "audio_files/test_audio/RockAndRoll_bad.wav")
file.improved_spectral_subtraction_filter()
file.plotter(channel=0, left=0, right=1, title="", xlabel="Время (в 1 / rate секундах)", ylabel="Амплитуда")
file.plotter(channel=0, left=0, right=1, title="", xlabel="Частота", ylabel="Амплитуда", is_spec=True)
# file.save()
#
#
# import numpy as np
# import scipy.io.wavfile as wav
#
# def add_noise_to_audio(input_file, output_file, noise_level):
#     # Загрузка аудиофайла
#     sample_rate, data = wav.read(input_file)
#
#     # Генерация шума с тем же размером и форматом, что и аудиофайл
#     noise = np.random.normal(0, noise_level, data.shape)
#
#     # Добавление шума к аудиофайлу
#     noisy_data = data + noise
#
#     # Ограничение значений аудиофайла в диапазоне от -32768 до 32767
#     noisy_data = np.clip(noisy_data, -32768, 32767)
#
#     # Сохранение измененного аудиофайла
#     wav.write(output_file, sample_rate, noisy_data.astype(np.int16))
#
# # Пример использования
# input_file = "audio_files/test_audio/RockAndRoll.wav"
# output_file = "audio_files/test_audio/RockAndRoll_bad.wav"
# noise_level = 400  # Уровень шума (можно изменить по вашему усмотрению)
#
# add_noise_to_audio(input_file, output_file, noise_level)