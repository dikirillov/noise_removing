from pydub import AudioSegment
import scipy
import numpy as np
import matplotlib.pyplot as plt


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


print(contains_speech("audio_files/interviews/sample_8.mp3"))
