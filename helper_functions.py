import os
import hashlib
from config import FLAGS, MAIN_PROMPTS


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
        elif user_input.lower() == "--help":
            print(MAIN_PROMPTS["--help"])
        else:
            return user_input


def make_unique_path(target_dir, archive_name):
    """
    Make the path unique by appending a number to the archive name.

    Parameters:
    target_dir (str): The target directory.
    archive_name (str): The archive name.

    Returns:
    str: The unique path.
    """
    path = os.path.join(target_dir, archive_name)
    if not os.path.exists(path):
        return path
    else:
        i = 1
        while True:
            new_path = f"{path}({i})"
            if not os.path.exists(new_path):
                return new_path
            i += 1
