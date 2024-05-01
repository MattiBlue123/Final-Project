import ast
import os
import re
from helper_functions import zinput
from config import FILE_HEADER_LENGTH


class PathValidator:
    def __init__(self, path):
        self.path = path

    def __is_valid_file(self, file_path):
        # checks if can open the file
        try:
            with open(file_path, 'r'):
                pass
        except IOError:
            raise IOError(f"File cannot be opened: {file_path}")
        return True

    def is_directory_empty(self):
        # checks if the directory is empty
        if os.path.isdir(self.path) and not os.listdir(self.path):
            raise ValueError(f"The specified directory {self.path} is empty. "
                             f"Can't add it to the archive")
        return False

    def validate_directory_for_archive(self):
        # checks if the directory is valid for archiving
        if self.is_directory_empty():
            raise ValueError(
                f"The specified directory {self.path} is empty."
                f" Can't add it to the archive")

        for name in os.listdir(self.path):
            file_path = os.path.join(self.path, name)
            if os.path.isfile(file_path):
                if not self.__is_valid_file(file_path):
                    raise ValueError(
                        f"Invalid file in directory: {file_path}")

        return True

    def __is_valid_path(self):
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError(f"File not found: {self.path}")

            # following checks are for directories
            if os.path.isdir(self.path):
                self.validate_directory_for_archive()

            # following checks are for files
            elif os.path.isfile(self.path):
                if not self.__is_valid_file(self.path):
                    raise ValueError(f"Invalid file: {self.path}")
        except Exception as e:
            print(f"Error validating file path: {e}")
            return False
        return True

    def validate_path(self):
        while not (self.__is_valid_path()):
            self.path = zinput("Enter valid path: ").strip('""')
        return self.path


class TargetDirectoryValidator:
    def __init__(self, target_directory):
        self.target_directory = target_directory

    def __is_valid_target_directory(self):
        try:
            if not os.path.exists(self.target_directory):
                raise FileNotFoundError(
                    f"Directory not found: {self.target_directory}")
            if not os.path.isdir(self.target_directory):
                raise NotADirectoryError(
                    f"Not a directory: {self.target_directory}")
        except Exception as e:
            print(f"Error validating target directory: {e}")
            return False
        return True

    def validate_target_directory(self):
        while not self.__is_valid_target_directory():
            self.target_directory = zinput(
                "Enter a valid target directory: ").strip('""')
        return self.target_directory


class UnitLengthValidator:
    def __init__(self, unit_length):
        self.unit_length = unit_length

    def __is_valid_unit_length(self):
        try:
            self.unit_length = int(self.unit_length)
            if self.unit_length <= 0:
                raise ValueError("Unit length must be a positive integer")
        except ValueError as ve:
            print(f"Error validating unit length: {ve}")
            return False
        return True

    def validate_unit_length(self):
        if self.unit_length == "":
            return ""
        while not self.__is_valid_unit_length():
            self.unit_length = zinput("Enter a valid unit length: ")
        return int(self.unit_length)


class ArchiveValidator:
    """
    Validates a given archive.
    Checks if in valid format.
    If it is, returns True. If not, tells what's wrong and returns False.
    """

    def __init__(self, archive, metadata):
        self.archive_path = archive
        self.metadata = metadata

    def get_all_files_data(self, files_list, current_metadata=None):
        """
        for each file in the archive's metadata:
        1. from metadata get the file's path in archive, file's pointer,
         file's header length, file's encoded size
        2. convert file's path in archive and  to sha - 1, find file's
        header in archive and check if matches.

        3. if not, print the key of that file with appropriate notification
        and :return False.
        4. if all files are valid, :return: True
        """
        if current_metadata is None:
            current_metadata = self.metadata

        for key, value in current_metadata.items():
            if isinstance(value, dict):
                if value["type"] == "file":
                    # creating a tuple for every file in the archive
                    header_hash = value["data hash"]
                    (files_list.append((key, header_hash,
                                        value["pointer"],
                                        value["encoded size"])))

                elif value["type"] == "folder":
                    self.get_all_files_data(files_list, value)
        return files_list

    def validate_archive(self):
        all_files_list = self.get_all_files_data([])
        with open(self.archive_path, 'rb') as f:
            for file in all_files_list:
                try:
                    # seeking end of file pointer
                    f.seek(file[2])
                    # seeking back to the start of the file's header
                    f.seek(-(file[3] + FILE_HEADER_LENGTH), os.SEEK_CUR)
                    # header found is bytes string that contains
                    header_found = f.read(FILE_HEADER_LENGTH)

                    header_in_metadata = file[1]
                    header_in_metadata = ast.literal_eval(header_in_metadata)
                    print(type(header_in_metadata))
                    print(f"the header: {file[1]}")
                    print(type(header_found))
                    print(f"header found: {header_found}")
                    if header_in_metadata != header_found:
                        raise ValueError(f"Invalid header for file: {file[0]}")
                except ValueError as ve:
                    print(ve)
                    return False
                except FileNotFoundError:
                    print(f"Error validating content of file: {file[0]} in "
                          f"archive {self.archive_path}")
                    return False
                except OSError:
                    print(f"Error Archive's metadata in wrong format")
                    return False
        return True

    @staticmethod
    def validate_path_in_archive_format(path):
        pattern = r"^/([\w\.\-\_ ]+/)*[\w\.\-\_ ]+$"
        if re.match(pattern, path):
            return True
        else:
            return False

    def validate_path_in_archive(self, path_in_archive_input):
        if not self.validate_path_in_archive_format(path_in_archive_input):
            return False
        # Parse the archive path into a list of keys
        parsed_path = self.parse_path_in_archive(path_in_archive_input)

        # Start with the root of the dictionary
        current_dict = self.metadata

        # For each key in the parsed path
        for key in parsed_path:
            # make sure key exist and is a file\folder
            if key in current_dict and isinstance(current_dict[key], dict):
                # if it's a folder, move to the next level of the dictionary
                current_dict = current_dict[key]
            else:
                # if file/folder not found in directory, raise exception
                return False

        # If you have checked all keys without returning False, return True
        return True

    @staticmethod
    def parse_path_in_archive(archive_path):
        # Remove leading and trailing slashes
        archive_path = archive_path.strip('/')
        # Split the path into a list of files/directories
        files = archive_path.split('/')
        return files
