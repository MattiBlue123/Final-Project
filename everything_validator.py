import os


class PathValidator:
    def __init__(self, path):
        self.path = path

    def has_subdirectory(self):
        for name in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path, name)):
                return True
        return False

    def is_directory_empty(self):
        if os.path.isdir(self.path) and not os.listdir(self.path):
            raise ValueError(f"The specified directory {self.path} is empty. "
                             f"Can't add it to the archive")

    def __is_valid_file(self, file_path):
        try:
            with open(file_path, 'r'):
                pass
        except IOError:
            raise IOError(f"File cannot be opened: {file_path}")
        return True

    def __is_valid_path(self):
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError(f"File not found: {self.path}")

            # following checks are for directories
            if os.path.isdir(self.path):
                if self.has_subdirectory():
                    raise ValueError(
                        f"Directory contains subdirectories: {self.path}")

                if os.path.isdir(self.path) and not os.listdir(self.path):
                    raise ValueError(
                        f"The specified directory {self.path} is empty. Can't add it to the archive")

                for name in os.listdir(self.path):
                    file_path = os.path.join(self.path, name)
                    if os.path.isfile(file_path):
                        if not self.__is_valid_file(file_path):
                            raise ValueError(
                                f"Invalid file in directory: {file_path}")

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
            self.path = input("Enter valid path or directory: ").strip('""')
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

    def validate_target_directory_input(self):
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

    def validate_unit_length_input(self):
        while not self.__is_valid_unit_length():
            self.unit_length = input("Enter a valid unit length: ")
        return int(self.unit_length)
