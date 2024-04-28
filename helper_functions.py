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


def create_file_metadata(path, unit_length, path_in_archive):
    """
    Create metadata for a file.

    Parameters:
    path (str): The path of the file.
    unit_length (int): The unit length.
    path_in_archive (str): The path in the archive.

    Returns:
    dict: The metadata of the file.
    """
    file_metadata = dict()
    file_metadata["type"] = "file"
    file_metadata["origin path"] = path
    file_metadata["path in archive"] = path_in_archive
    file_metadata["pointer"] = None
    file_metadata["header length"] = None
    file_metadata["encoded size"] = None
    file_metadata["unit length"] = unit_length
    file_metadata["data hash"] = None
    file_metadata["original size"] = os.path.getsize(path)
    return file_metadata


def create_directory_metadata(path, unit_length, path_in_archive):
    """
    Create metadata for a directory.

    Parameters:
    path (str): The path of the directory.
    unit_length (int): The unit length.
    path_in_archive (str): The path in the archive.

    Returns:
    dict: The metadata of the directory.
    """
    directory_metadata = dict()
    directory_metadata["type"] = "folder"
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            directory_metadata[file] = create_directory_metadata(
                file_path, unit_length, path_in_archive + "/" + file)
        else:
            directory_metadata[file] = create_file_metadata(
                file_path, unit_length, path_in_archive + "/" + file)
    return directory_metadata


def create_metadata(path, unit_length, path_in_archive=""):
    """
    Create metadata for a file or directory.

    Parameters:
    path (str): The path of the file or directory.
    unit_length (int): The unit length.
    path_in_archive (str): The path in the archive.

    Returns:
    dict: The metadata of the file or directory.
    """
    if os.path.isdir(path):
        return create_directory_metadata(path, unit_length,
                                         path_in_archive)
    else:
        return create_file_metadata(path, unit_length,
                                    path_in_archive)


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
