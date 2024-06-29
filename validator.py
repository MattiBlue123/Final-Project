import os
import re
from typing import Dict, Union, List

from helper_functions import zinput


class PathValidator:
    """
    The PathValidator class is responsible for
     validating a file or directory path.
    """

    def __init__(self, path: str):
        """
        Initialize the PathValidator with the path to be validated.

        :param:
        path (str): The path to be validated
        """
        self.path = path

    @staticmethod
    def __is_valid_file(file_path: str) -> bool:
        """
        :param file_path: The path of the file to be checked.
        :return: True if the file can be opened, False otherwise.
        """
        # Try to open the file
        try:
            with open(file_path, 'r'):
                pass
        except IOError:
            raise IOError(f"File cannot be opened: {file_path}")
        return True

    def __is_directory_empty(self) -> bool:
        """
        Check if a directory is empty.

        :return: False if the directory is not empty, True otherwise.
        """
        # Check if the directory is empty
        if os.path.isdir(self.path) and not os.listdir(self.path):
            raise ValueError(f"The specified directory {self.path} is empty. "
                             f"Can't add it to the archive")
        return False

    def validate_directory_for_archive(self) -> bool:
        """
        Check if a directory is valid for archiving.

        :return: True if the directory is valid for archiving, False otherwise.
        """
        # Check if the directory is empty
        if self.__is_directory_empty():
            raise ValueError(
                f"The specified directory {self.path} is empty."
                f" Can't add it to the archive")

        # Check if all files in the directory are valid
        for name in os.listdir(self.path):
            file_path = os.path.join(self.path, name)
            if os.path.isfile(file_path):
                if not self.__is_valid_file(file_path):
                    raise ValueError(
                        f"Invalid file in directory: {file_path}")

        return True

    def __is_valid_path(self) -> bool:
        """
        Check if a path is valid.

        :return: True if the path is valid, False otherwise.
        """
        try:
            # Check if the path exists
            if not os.path.exists(self.path):
                raise FileNotFoundError(f"File not found: {self.path}")

            # If the path is a directory, validate it for archiving
            if os.path.isdir(self.path):
                self.validate_directory_for_archive()

            # If the path is a file, validate it
            elif os.path.isfile(self.path):
                if not self.__is_valid_file(self.path):
                    raise ValueError(f"Invalid file: {self.path}")
        except Exception as e:
            print(f"Error validating file path: {e}")
            return False
        return True

    def validate_path(self) -> str:
        """
        Validate a path. If the path is not valid,
         ask the user to enter a valid path.

        :return: The valid path.
        """
        while not (self.__is_valid_path()):
            self.path = zinput("Enter valid path: ").strip('""')
        return self.path


class TargetDirectoryValidator:
    """
    The TargetDirectoryValidator class is responsible for validating
    a target directory.
    """

    def __init__(self, target_directory: str):
        """
        Initialize the TargetDirectoryValidator with the target
         directory to be validated.

        :param target_directory: The target directory to be validated.
        """
        self.target_directory = target_directory

    def __is_valid_target_directory(self) -> bool:
        """
        Check if a target directory is valid.

        :return: True if the target directory is valid, False otherwise.
        """
        try:
            # Check if the target directory exists
            if not os.path.exists(self.target_directory):
                raise FileNotFoundError(
                    f"Directory not found: {self.target_directory}")
            # Check if the target directory is a directory
            if not os.path.isdir(self.target_directory):
                raise NotADirectoryError(
                    f"Not a directory: {self.target_directory}")
        except Exception as e:
            print(f"Error validating target directory: {e}")
            return False
        return True

    def validate_target_directory(self) -> str:
        """
        Validate a target directory. If the target directory is not valid,
        ask the user to enter a valid target directory.

        :return: The valid target directory.
        """
        # Keep asking for a valid target directory until one is provided
        while not self.__is_valid_target_directory():
            self.target_directory = zinput(
                "Enter a valid target directory: ").strip('""')
        return self.target_directory


class UnitLengthValidator:
    def __init__(self, unit_length: int):
        self.unit_length = unit_length

    def __is_valid_unit_length(self) -> bool:
        try:
            self.unit_length = int(self.unit_length)
            if self.unit_length <= 0:
                raise ValueError("Unit length must be a positive integer")
        except ValueError as ve:
            print(f"Error validating unit length: {ve}")
            return False
        return True

    def validate_unit_length(self) -> Union[int, str]:
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

    def __init__(self, archive: str, metadata: Dict):
        self.archive_path = archive
        self.metadata = metadata

    def validate_metadata(self, curr_dict: Dict = None) -> bool:
        """
        Validates that an archive's metadata has all essential keys
        and that the values' types are as expected.
        If it's the given metadata, it doesn't need to have a "type" key.
        :param curr_dict: The metadata then it's nested dicts.
        :return: bool
        """
        if curr_dict is None:
            curr_dict = self.metadata

        file_required_keys = ["type", "pointer", "unit length",
                              "encoded size", "original size"]

        # Iterate over all key-value pairs in the current dictionary
        for key, value in curr_dict.items():
            if not curr_dict == self.metadata:
                if "type" not in curr_dict:
                    print(f"Missing key: type in {curr_dict}")
                    return False

            # Check if the key is a string
            if not isinstance(key, str):
                print(f"Invalid key type: {key} is not a string")
                return False

            # validates the value type is int for the keys below
            if key in ["pointer", "unit length", "encoded size",
                       "original size"] and not isinstance(value, int):
                print(f"Invalid value type: {value} is not an integer")
                return False

            # "type" could also be a file/folders name. if it is, then it's
            # value would be a dict.
            if key == "type" and not (isinstance(value, dict)):

                # if it's a file, it should have all the required keys
                if value == "file":
                    for required_key in file_required_keys:
                        if required_key not in curr_dict:
                            print(f"Missing key: {required_key} in file"
                                  f" {curr_dict}")
                            return False
                # if the value of the key "type" is not "file", not "folder"
                # and it's not file/folder name - it's an invalid key
                elif value != "folder":
                    print(
                        f"Invalid type:{type(value)} \n{value} for key: {key}")
                    return False
                return True

            # If the value is a dictionary, recursively validate it
            if isinstance(value, dict):
                if not self.validate_metadata(value):
                    return False

        return True

    @staticmethod
    def validate_path_in_archive_format(path: str) -> bool:
        pattern = r"^/([\w\.\-\_ ]+/)*[\w\.\-\_ ]+$"
        if re.match(pattern, path):
            return True
        else:
            return False

    def validate_path_in_archive(self, path_in_archive_input: str) -> bool:
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
    def parse_path_in_archive(archive_path: str) -> List:
        """
        Parse the path in the archive into a list of keys.
        :param archive_path:
        :return:
        """
        # Remove leading and trailing slashes
        archive_path = archive_path.strip('/')
        # Split the path into a list of files/directories
        files = archive_path.split('/')
        return files
