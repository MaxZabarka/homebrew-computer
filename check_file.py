import os


def check_file(file_path):
    if os.path.exists(file_path):
        if os.path.isfile(file_path):
            return file_path
        elif os.path.isdir(file_path):
            print(file_path + " is a directory")
        else:
            print(file_path + " could not be opened")
    else:
        print("File or directory not found")
        exit()
