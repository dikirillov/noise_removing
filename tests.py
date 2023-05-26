import unittest
import subprocess


class TestMyProgram(unittest.TestCase):
    def test_program_output(self):
        output = subprocess.check_output(["python", "main.py"], universal_newlines=True)
        self.assertEqual(output.strip(), "Error: Invalid arguments.\n"
                           "Please, give 2 filenames and list of filters.\n"
                           "Supported filters: band, exp, sub, impr_sub.\n"
                           "Supported file types: mp3, wav.")

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


if __name__ == '__main__':
    unittest.main()
