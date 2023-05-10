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


# функция, выполняющая очистку от шума высоких и низких частот
def bandpass_filter(src):
    if ".mp3" in src:
        src = from_mp3_to_wav(src)

    rate, data = scipy.io.wavfile.read(src)
    channels_cnt = 1
    window_size = rate
    data_size = len(data)
    try:
        channels_cnt = data.shape[1]
    except:
        pass

    for channel in range(channels_cnt):
        pos = 0
        while pos + window_size < data_size:
            transformed_audio = np.fft.fft(data[:, channel][pos: pos + window_size])
            size = transformed_audio.size
            transformed_audio[:200] = 0
            transformed_audio[-200:] = 0
            transformed_audio[7000:size // 2] = 0
            transformed_audio[size // 2:-7000] = 0
            data[:, channel][pos: pos + window_size] = np.fft.ifft(transformed_audio).real
            pos += window_size

    scipy.io.wavfile.write(src[:-4] + "_correct" + ".wav", rate=rate, data=data)


# функция, хорошо очищающая высокочастотный и никочастотный шум
# также она выполняет сглаживание остального диапазона
def exponentional_filter(src):
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
            filter = np.exp(-1.5 * alpha * (np.minimum(inds, n - inds) ** 2) / 2)
            transformed_audio *= filter

            data[:, channel][pos: pos + n] = np.fft.ifft(transformed_audio).real
            pos += window_size

    scipy.io.wavfile.write(src[:-4] + "_correct" + ".wav", rate=rate, data=data)


# функция, очищающая периодический шум
# по первой 0.1 секунду записи
def spectral_subtraction_filter(src):
    if ".mp3" in src:
        src = from_mp3_to_wav(src)

    rate, data = scipy.io.wavfile.read(src)
    channels_cnt = 1
    window_size = int(rate * 0.1)
    data_size = len(data)
    try:
        channels_cnt = data.shape[1]
    except:
        pass

    for channel in range(channels_cnt):
        pos = 0
        noise = np.fft.fft(data[:, channel][:window_size])
        max_level = max(noise)
        while pos + window_size < data_size:
            transformed_audio = np.fft.fft(data[:, channel][pos: pos + window_size])
            if max(transformed_audio) < max_level:
                noise = transformed_audio
                max_level = max(transformed_audio)

            pos += window_size

        pos = 0
        while pos + window_size < data_size:
            transformed_audio = np.fft.fft(data[:, channel][pos: pos + window_size]) - noise
            data[:, channel][pos: pos + window_size] = np.fft.ifft(transformed_audio).real
            pos += window_size

    scipy.io.wavfile.write(src[:-4] + "_correct" + ".wav", rate=rate, data=data)


spectral_subtraction_filter("audio_files/interviews/sample_11.wav")
