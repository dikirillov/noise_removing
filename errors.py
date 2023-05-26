errors = {
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
