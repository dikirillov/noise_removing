from pydub import AudioSegment
import scipy
import numpy as np
import matplotlib.pyplot as plt


# функция для целочисленного деления с округлением вверх
def div_round_up(value, divider):
    return (value + divider - 1) // divider


# функция для преобразования mp3 в wav файл, с ним удобнее работать
def from_mp3_to_wav(src):
    dst = src.replace(".mp3", ".wav")

    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")
    return src.replace("mp3", "wav")


# функция, определяющая наличие речи
def contains_speech(src):
    if ".mp3" in src:
        src = from_mp3_to_wav(src)

    rate, data = scipy.io.wavfile.read(src)
    try:
        if data.shape[1]:
            data = data.T[0]
    except:
        data = data.T

    fourier = np.fft.fft(data)
    return max(fourier) > 1e7


# функция, очищающая высокочастотный и никочастотный шум
# также она выполняет сглаживание остального диапазона
def bad_frequency_cleaner(src):
    if ".mp3" in src:
        src = from_mp3_to_wav(src)

    rate, data = scipy.io.wavfile.read(src)
    channels_cnt = 1
    window_size = int(rate * 1.5)
    data_size = len(data)
    try:
        channels_cnt = data.shape[1]
    except:
        pass

    for channel in range(channels_cnt):
        pos = 0
        while pos + window_size < data_size:
            n = window_size
            if pos + 2 * window_size > data_size:
                n = data_size - pos

            transformed_audio = np.fft.fft(data[:, channel][pos: pos + n])
            inds = np.arange(n)
            alpha = 0.0000001
            filter = np.exp(-1.5 * alpha * (np.minimum(inds, n - inds) ** 2) / 2)[:n]
            transformed_audio *= filter

            data[:, channel][pos: min(len(data), pos + n)] = np.fft.ifft(transformed_audio).real
            pos += window_size

    scipy.io.wavfile.write(src[:-4] + "_correct" + ".wav", rate=rate, data=data)
    return


print(bad_frequency_cleaner("audio_files/test_audio/RockAndRoll.wav"))
