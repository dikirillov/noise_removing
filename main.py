import sys
from errors import exit_with_error
from filters import AudioFile


def is_audio_file(file_name):
    return file_name[-4:] in [".mp3", ".wav"]


def validate(kwargs_list):
    if not kwargs_list:
        exit_with_error("no_args")
    defined_args = {"band", "exp", "sub", "impr_sub"}

    offset = 1
    if not is_audio_file(kwargs_list[0]):
        exit_with_error("bad_input_file", kwargs_list[0])

    if len(kwargs_list) > 1 and is_audio_file(kwargs_list[1]):
        offset = 2

    for index in range(offset, len(kwargs_list)):
        if (kwargs_list[index] not in defined_args) and (not kwargs_list[index].isdigit()):
            exit_with_error("bad_filter_name", kwargs_list[index])

    return offset


if __name__ == "__main__":
    kwargs = sys.argv[1:]
    filters_offset = validate(kwargs)
    audio = None
    if filters_offset == 1:
        audio = AudioFile(kwargs[0])
    else:
        audio = AudioFile(kwargs[0], kwargs[1])

    filters = {
        "band": audio.bandpass_filter,
        "exp": audio.exponentional_filter,
        "sub": audio.spectral_subtraction_filter,
        "impr_sub": audio.improved_spectral_subtraction_filter,
    }

    kwargs_size = len(kwargs)
    index = filters_offset
    while index < kwargs_size:
        if kwargs[index] not in filters:
            exit_with_error("bad_filter_name", kwargs[index])

        left = None
        right = None
        cur_filter = filters[kwargs[index]]
        if index + 1 < kwargs_size and kwargs[index + 1].isdigit():
            index += 1
            left = int(kwargs[index])
            if index + 1 < kwargs_size and kwargs[index + 1].isdigit():
                index += 1
                right = int(kwargs[index])

        cur_filter(left, right)
        index += 1

    audio.save()
    print("Saved cleared file to the", audio.output_file_name)
