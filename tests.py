import os
import unittest
import subprocess
from errors import errors


class TestMyProgram(unittest.TestCase):
    def tests_valid_inputs(self):
        output = subprocess.check_output(["python", "main.py"], universal_newlines=True)
        self.assertEqual(output.strip(), errors["no_args"][1])

        output = subprocess.check_output(["python", "main.py", "audio_files/test_audio/RockAndRoll.wav"],
                                         universal_newlines=True)
        self.assertEqual(output.strip(), "Saved cleared file to the audio_files/test_audio/RockAndRoll_correct.wav")

        output = subprocess.check_output(["python", "main.py", "audio_files/test_audio/RockAndRoll.mp3"],
                                         universal_newlines=True)
        self.assertEqual(output.strip(), "Saved cleared file to the audio_files/test_audio/RockAndRoll_correct.mp3")

        output = subprocess.check_output(["python", "main.py", "audio_files/test_audio/RockAndRoll.wav",
                                          "audio_files/test_audio/RockAndRoll.mp3"],
                                         universal_newlines=True)
        self.assertEqual(output.strip(), "Saved cleared file to the audio_files/test_audio/RockAndRoll.mp3")

        output = subprocess.check_output(["python", "main.py", "audio_files/test_audio/RockAndRoll.wav", "band",
                                          "0", "1"],
                                         universal_newlines=True)
        self.assertEqual(output.strip(), "Saved cleared file to the audio_files/test_audio/RockAndRoll_correct.wav")

        output = subprocess.check_output(["python", "main.py", "audio_files/test_audio/RockAndRoll.wav", "band",
                                          "1"],
                                         universal_newlines=True)
        self.assertEqual(output.strip(), "Saved cleared file to the audio_files/test_audio/RockAndRoll_correct.wav")

        output = subprocess.check_output(["python", "main.py", "audio_files/test_audio/RockAndRoll.wav", "band",
                                          "1", "exp"],
                                         universal_newlines=True)
        self.assertEqual(output.strip(), "Saved cleared file to the audio_files/test_audio/RockAndRoll_correct.wav")

        output = subprocess.check_output(["python", "main.py", "help"],
                                         universal_newlines=True)
        self.assertEqual(output.strip(), errors["help"][1])

    def tests_invalid_filenams(self):
        f = open(os.devnull, "w")
        test_proc = subprocess.Popen(["python", "main.py", "1"], universal_newlines=True, stdout=f)
        test_proc.wait()
        self.assertEqual(test_proc.returncode, errors["bad_input_file"][0])
        f.close()

    def test_invalid_filter(self):
        f = open(os.devnull, "w")
        test_proc = subprocess.Popen(["python", "main.py", "audio_files/test_audio/RockAndRoll.wav", "error"], universal_newlines=True, stdout=f)
        test_proc.wait()
        self.assertEqual(test_proc.returncode, errors["bad_filter_name"][0])

        test_proc = subprocess.Popen(["python", "main.py", "audio_files/test_audio/RockAndRoll.wav", "band", "0", "1", "1"], universal_newlines=True, stdout=f)
        test_proc.wait()
        self.assertEqual(test_proc.returncode, errors["bad_filter_name"][0])
        f.close()

    def tests_invalid_boarder(self):
        f = open(os.devnull, "w")
        test_proc = subprocess.Popen(["python", "main.py", "audio_files/test_audio/RockAndRoll.wav", "band", "10", "20"], universal_newlines=True, stdout=f)
        test_proc.wait()
        self.assertEqual(test_proc.returncode, errors["bad_boards"][0])
        f.close()


if __name__ == '__main__':
    unittest.main()
