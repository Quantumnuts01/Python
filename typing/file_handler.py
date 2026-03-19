def read_file_as_string(filename):
    file_string = ""
    try:
        with open(filename) as f:
            file_string = f.read()
    except FileNotFoundError:
        print("Error, file not found!")
    return file_string

def read_lines_from_file(filename):
    lines = []
    lines = read_file_as_string(filename).strip().split("\n")
    return lines

def write_to_file(filename, string):
    try:
        with open(filename, "a") as f:
            f.write(string)
    except FileNotFoundError:
        print("Error, file not found!")

