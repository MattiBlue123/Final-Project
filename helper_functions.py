import os
import hashlib
from config import FLAGS
def hash_data(data):
    sha1 = hashlib.sha1()
    if isinstance(data, str):
        sha1.update(data.encode('utf-8'))  # encode the string to bytes
    else:
        sha1.update(data)  # data is already bytes
    return sha1.digest()


def iterate_nested_dict(nested_dict):
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            # If value is a dictionary, recursively process it
            iterate_nested_dict(value)
        else:
            # If value is not a dictionary, print the key and value
            print(f"{key}: {value}, {type(value)}")


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
            if path_in_archive in directory_metadata.values():
                raise ValueError(f"A file with the same name already "
                                 f"exists: {path_in_archive}")
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
