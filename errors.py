errors = {
    "help": (0, "The first parameter is the input audio file name, and the second parameter is the output \n"
                "audio file name (optional). Next, you need to provide the names of the filters. The available \n"
                "parameters are:\n\n"
                "band - for applying the Bandpass filter\n"
                "exp - for applying the Exponential filter\n"
                "sub - for applying the Spectral subtraction filter\n"
                "impr_sub - for applying the Improved spectral subtraction filter.\n\n"
                "After each filter you can optionally provide two integers representing the boundaries of the \n"
                "timestamp interval of the audio recording to which the filter will be applied. If only one integer is \n"
                "provided, it will be interpreted as the left boundary of the segment, and the end of the \n"
                "recording will serve as the right boundary. If no boundary values are provided, the filter will\n"
                "be applied to the entire audiofile."),
    "no_args": (0, "Error: Invalid arguments.\n"
                   "Please, give 2 filenames and list of filters.\n"
                   "Supported filters: band, exp, sub, impr_sub.\n"
                   "Supported file types: mp3, wav."),
    "bad_input_file": (1, "Error: Invalid input file format, use mp3 or wav file:"),
    "bad_filter_name": (2, "Unknown filter name:"),
    "broken_input_file": (3, "Unable to read input file:"),
    "broken_output_file": (4, "Unable to save output file:"),
    "bad_boards": (5, "Invalid boarder of given timestamp interval"),
}


def exit_with_error(err, msg=None):
    if msg:
        print(errors[err][1], msg)
    else:
        print(errors[err][1])
    exit(errors[err][0])
