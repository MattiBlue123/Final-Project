import os
import re

from helper_functions import hash_data


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
                f"The specified directory {self.path} is empty. Can't add it to the archive")

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
            self.path = input("Enter valid path: ").strip('""')
        return self.path

    def validate_path_in_archive(self, path_in_archive, general_metadata):
        for key, value in general_metadata.items():
            if key == "path in_archive" and value == path_in_archive:
                return True
            elif isinstance(value, dict):
                if self.validate_path_in_archive(path_in_archive, value):
                    return True
        return False


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
            self.target_directory = input(
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
        if self.unit_length is "":
            return ""
        while not self.__is_valid_unit_length():
            self.unit_length = input("Enter a valid unit length: ")
        return int(self.unit_length)


class ArchiveValidator:
    """
    Validates a given archive.
    Checks if in valid format.
    If it is, returns True. If not, tells what's wrong and returns False.
    """

    def __init__(self, archive, metadata):
        self.archive = archive
        self.metadata = metadata

    def get_all_files_data(self, files_list):
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
        for key, value in self.metadata.items():
            if isinstance(value, dict):
                if value["type"] == "file":
                    # creating a tuple for every file in the archive
                    header_hash = hash_data(
                        value["path in archive"].encode('utf-8'))
                    (files_list.append((key, header_hash,
                                       value["pointer"],
                                       value["encoded size"],
                                       value["header length"])))

                elif value["type"] == "folder":
                    self.get_all_files_data(files_list)
        return files_list

    def validate_metadata(self):
        """
        Validates that the metadata has all the necessary fields
        :return: True if all fields are present, False otherwise

        fields:
            file_metadata["path in archive"] = path_in_archive
            file_metadata["pointer"] = None
            file_metadata["header length"] = None
            file_metadata["encoded size"] = None
            file_metadata["unit length"] = unit_length
            file_metadata["data hash"] = None
            file_metadata["original size"] = os.path.getsize(path)
            file_metadata["original size"] = bytes_num
            file_metadata["header length"] = header_length
            file_metadata["encoded size"] = encoded_content_size
            file_metadata["data hash"] = hashed_content
        """
        metadata = self.metadata.decode('utf-8')
        required_keys = {
            "path in archive": str,
            "pointer": int,
            "header length": int,
            "encoded size": int,
            "unit length": int,
            "data hash": None,  # exists, no type check
            "original size": int
        }

        for key, value in metadata.items():
            if isinstance(value, dict):
                if value["type"] == "file":
                    for required_key, required_type in required_keys.items():
                        if required_key not in value:
                            print(f"Missing key in metadata: {required_key}")
                            return False
                        if required_type is not None and not isinstance(
                                value[required_key], required_type):
                            print(
                                f"Invalid type for key {required_key}:"
                                f" expected {required_type},"
                                f" got {type(value[required_key])}")
                            return False
        return True

    def validate_archive(self):
        all_files_list = self.get_all_files_data([])
        with open(self.archive, 'rb') as f:
            for file in all_files_list:
                try:
                    f.seek(file[2])
                    f.seek(-(file[3] + file[4]), os.SEEK_CUR)
                    if file[1] != f.read(file[4]):
                        raise ValueError(f"Invalid header for file: {file[0]}")
                except ValueError as ve:
                    print(ve)
                    return False
                except FileNotFoundError:
                    print(f"Error validating content of file: {file[0]} in "
                          f"archive {self.archive}")
                    return False
        return True

    @staticmethod
    def validate_path_in_archive_format(path):
        pattern = r"^/([\w\.\-\_ ]+/)*[\w\.\-\_ ]+$"
        if re.match(pattern, path):
            return True
        else:
            return False
