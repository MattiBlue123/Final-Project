import os
import re


def recursive_items(dictionary, path='', start=''):
    for key, value in dictionary.items():
        new_path = f'{path}/{key}' if path else key
        if isinstance(value, dict):
            # If the dictionary has any nested dictionaries, don't print the current path
            if any(isinstance(v, dict) for v in value.values()):
                recursive_items(value, new_path, start)
            elif new_path.startswith(start):
                print(new_path)
        else:
            continue


def validate_path_format(path):
    pattern = r"^/([\w\.\-\_ ]+/)*[\w\.\-\_ ]+$"
    if re.match(pattern, path):
        return True
    else:
        return False


def parse_archive_path(archive_path):
    # Remove leading and trailing slashes
    archive_path = archive_path.strip('/')
    # Split the path into a list of files/directories
    files = archive_path.split('/')
    return files


def validate_path_in_archive(archive_path, dictionary):
    if not validate_path_format(archive_path):
        raise ValueError("Invalid path format")
    # Parse the archive path into a list of keys
    parsed_path = parse_archive_path(archive_path)

    # Start with the root of the dictionary
    current_dict = dictionary

    # For each key in the parsed path
    for key in parsed_path:
        # make sure key exist and is a file\folder
        if key in current_dict and isinstance(current_dict[key], dict):
            # if it's a folder, move to the next level of the dictionary
            current_dict = current_dict[key]
        else:
            # If the key does not exist or its value is not a dictionary, return False
            raise ValueError("Invalid path in archive")

    # If you have checked all keys without returning False, return True
    return True


example_dict = {"address": {
    "street": "123 Main St",
    "city": "Anytown",
    "state": "Anystate",
    "zip": "12345",
    "more": {"yes": "no", "stuff": {"thins": 123}}
}
}
#
# path = "/folder1folder2folder3.ue/my file.txt.../"
# try:
#     if validate_path_in_archive(path, example_dict):
#         print("Valid path")
#     else:
#         print("Invalid path")
# except ValueError as e:
#     print(e)
#     input("try again: ")

key = "folder1"
target_dir = r"C:\Users\zohar\OneDrive\Desktop"
directory_path = os.path.join(target_dir, key)
os.mkdir(directory_path)
