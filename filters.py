import os
from pydub import AudioSegment
import scipy
import numpy as np
import matplotlib.pyplot as plt
import sys
import re


def exit_with_error(code, error_msg):
    print("Error:", error_msg)
    exit(code)


class AudioFile:
    def __init__(self, arg1, arg2=None):
        """
        initializer of AudioFile. 2 different types of arguments:
            1) arg1 - input file name, arg2 - output file name
            2) arg1 - rate, arg2 - data (check output of scipy.io.wavfile.read)
        """
        if type(arg1) == str:
            if arg2 is None:
                arg2 = re.sub(r"\.", r"_correct.", arg1)

            self.input_file_name = arg1
            self.output_file_name = arg2
            if '.mp3' in arg1:
                dst = arg1.replace(".mp3", ".wav")
                try:
                    sound = AudioSegment.from_mp3(arg1)
                    sound.export(dst, format="wav")
                    self.rate, self.data = scipy.io.wavfile.read(dst)
                    os.remove(dst)
                except:
                    print("Error: Unable to read input file")
                    sys.exit(2)
            else:
                self.rate, self.data = scipy.io.wavfile.read(arg1)
        else:
            self.rate = arg1
            self.data = arg2

        self.channels_cnt = 1
        try:
            self.channels_cnt = self.data.shape[1]
        except:
            pass

    def save(self):
        """
        saves file to self.output_file_name
        """
        try:
            if ".wav" in self.output_file_name:
                scipy.io.wavfile.write(self.output_file_name, rate=self.rate, data=self.data)
            else:
                dst = self.output_file_name
                dst.replace("mp3", "wav")
                scipy.io.wavfile.write(dst, rate=self.rate, data=self.data)
                AudioSegment.from_wav(dst).export(self.output_file_name, format="mp3")
                os.remove(dst)
        except:
            print("Error: Unable to save output file")
            sys.exit(3)

    def get_boarders(self, left, right):
        """
        calculates boarders between given seconds of the record
        """
        start = 0
        end = len(self.data)
        if left:
            start = left * self.rate
        if right:
            end = right * self.rate

        if start < 0 or end > len(self.data):
            print("Error: Invalid right timestamp of given interval")
            sys.exit(4)
        return start, end

    def bandpass_filter(self, left=None, right=None):
        """
        function that reduces high and low frequency noise
        """
        window_size = self.rate
        start, end = self.get_boarders(left, right)

        for channel in range(self.channels_cnt):
            pos = start
            while pos + window_size < end:
                transformed_audio = np.fft.fft(self.data[:, channel][pos: pos + window_size])
                size = transformed_audio.size
                transformed_audio[:200] = 0
                transformed_audio[-200:] = 0
                transformed_audio[5000:size // 2] = 0
                transformed_audio[size // 2:-5000] = 0
                self.data[:, channel][pos: pos + window_size] = np.fft.ifft(transformed_audio).real
                pos += window_size

    def exponentional_filter(self, left=None, right=None):
        """
        function that cleans the spectrum using a exponential filter.
        as a result, high and low frequencies are seriously cleared,
        the rest of the frequencies are smoothed out
        """
        window_size = int(self.rate * 1.5)
        start, end = self.get_boarders(left, right)

        for channel in range(self.channels_cnt):
            pos = start
            while pos + window_size < end:
                n = window_size
                if pos + 2 * window_size > end:
                    n = end - pos

                transformed_audio = np.fft.fft(self.data[:, channel][pos: pos + n])
                inds = np.arange(n)
                alpha = 0.0000001
                exp_filter = np.exp(-1.5 * alpha * (np.minimum(inds, n - inds) ** 2) / 2)
                transformed_audio *= exp_filter

                self.data[:, channel][pos: pos + n] = np.fft.ifft(transformed_audio).real
                pos += window_size

    def spectral_subtraction_filter(self, left=None, right=None):
        """
        this function finds the quietest 0.1 second and subtracts it from the whole record
        """
        window_size = int(self.rate * 0.1)
        start, end = self.get_boarders(left, right)

        for channel in range(self.channels_cnt):
            pos = start
            noise = np.fft.fft(self.data[:, channel][:window_size])
            min_level = np.mean(np.abs(noise))
            while pos + window_size < end:
                transformed_audio = np.fft.fft(self.data[:, channel][pos: pos + window_size])
                if np.mean(np.abs(transformed_audio)) < min_level:
                    noise = transformed_audio
                    min_level = np.mean(np.abs(transformed_audio))

                pos += window_size

            pos = start
            while pos + window_size < end:
                transformed_audio = np.fft.fft(self.data[:, channel][pos: pos + window_size]) - noise
                self.data[:, channel][pos: pos + window_size] = np.fft.ifft(transformed_audio).real
                pos += window_size

    def improved_spectral_subtraction_filter(self, left=None, right=None):
        """
        this function finds the quietest is an improved version of spectral_subtraction_filter
        it works pretty much the same, but the cleanup is applied to 0.1 second fragments
        """
        window_size = int(self.rate * 0.1)
        window_size -= window_size % 10
        start, end = self.get_boarders(left, right)

        for channel in range(self.channels_cnt):
            external_pos = start
            while external_pos + window_size < end:
                internal_audio_data = np.array([self.data[:, channel][external_pos:external_pos + window_size]]).T
                internal_audio_file = AudioFile(window_size, internal_audio_data)
                internal_audio_file.spectral_subtraction_filter()

                self.data[external_pos:external_pos + window_size] = internal_audio_file.data
                external_pos += window_size

    def plotter(self, channel, left, right, title, xlabel, ylabel, is_spec=False):
        plot_data = self.data[:, channel][left * self.rate:right * self.rate]
        if is_spec:
            transformed_audio = np.fft.fft(plot_data)
            size = transformed_audio.size
            plot_data = transformed_audio[10:size // 2]
        plt.plot(plot_data)
        plt.title(title, fontsize=40)
        plt.xlabel(xlabel, fontsize=40)
        plt.xticks(fontsize=25)
        plt.ylabel(ylabel, fontsize=40)
        plt.yticks(fontsize=25)
        plt.show()
