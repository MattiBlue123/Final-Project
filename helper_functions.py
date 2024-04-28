import os
import hashlib
from config import FLAGS
import re


def hash_data(data):
    sha1 = hashlib.sha1()
    if isinstance(data, str):
        sha1.update(data.encode('utf-8'))  # encode the string to bytes
    else:
        sha1.update(data)  # data is already bytes
    return sha1.digest()


def zinput(prompt):
    """
    Get user input with support for graceful exit via "exit" command.

    """
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'exit':
            print("Exiting program.")
            FLAGS["exit_flag"] = True
            exit(0)
        elif user_input.lower() == "back":
            FLAGS["back_flag"] = True
            return ""
        else:
            return user_input


def parse_archive_path(archive_path):
    # Remove leading and trailing slashes
    archive_path = archive_path.strip('/')
    # Split the path into a list of files/directories
    files = archive_path.split('/')
    return files


def validate_path_format(path):
    pattern = r"^/([\w\.\-\_ ]+/)*[\w\.\-\_ ]+$"
    if re.match(pattern, path):
        return True
    else:
        return False



