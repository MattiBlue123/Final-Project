import os


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


class TargetDirectoryValidator:
    def __init__(self, target_directory):
        self.target_directory = target_directory

    def __is_valid_target_directory(self):
        try:
            if not os.path.exists(self.target_directory):
                raise FileNotFoundError(
                    f"Directory not found: {self.target_directory}")
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
        if unit_length == "":
            unit_length = 1
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
        while not self.__is_valid_unit_length():
            self.unit_length = input("Enter a valid unit length: ")
        return int(self.unit_length)
