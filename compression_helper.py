import os
from pathlib import Path
import struct


class RunLengthEncoder:
    def __init__(self, file_path, unit_length):
        self.file_path = file_path
        self.file_name = Path(file_path).stem
        self.unit_length = unit_length

    def create_header(self, bytes_num):

        # Get the file's name without the extension
        file_name = Path(self.file_path).stem + "|" + str(bytes_num)

        # Convert the file's name to binary format
        header = bytes(file_name, 'utf-8')

        # Create a header that contains the binary representation of the
        # file's name and the length of the file's content

        return header

    def encode(self):
        # open the file in binary mode
        with open(self.file_path, 'rb') as f:
            content = f.read()
            #  creating header file's name and the content's length
            bytes_num = len(content)
            header = self.create_header(bytes_num)
            encoded = header
            count = 1

            if self.unit_length >= bytes_num:
                encoded += content
                return encoded

            # encode the content
            for i in range(0, bytes_num - (bytes_num % self.unit_length),
                           self.unit_length):
                # making sure next unit exists
                if i + self.unit_length >= bytes_num:
                    break
                curr_unit = content[i:i + self.unit_length]
                next_unit = content[i + self.unit_length:i +
                                                         2 * self.unit_length]
                if curr_unit == next_unit:
                    count += 1
                else:
                    encoded += struct.pack('B', count)
                    encoded += curr_unit
                    count = 1
            # encode the last unit
            encoded += struct.pack('B', count)
            encoded += curr_unit
            # encoding the remaining bytes (outside the unit length)
            if bytes_num % self.unit_length != 0:
                encoded += struct.pack('B', count)
                encoded += content[bytes_num -
                                   (bytes_num % self.unit_length):]

            return encoded


class PathValidator:
    def __init__(self, path):

        self.path = path

    def has_subdirectory(self):
        for name in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path, name)):
                return True
        return False

    def __is_valid_path_or_dir(self):
        try:
            if not os.path.exists(self.path):
                raise FileNotFoundError(f"File not found: {self.path}")
            if os.path.isdir(self.path) and self.has_subdirectory():
                raise ValueError(f"Directory contains subdirectories: {self.path}")
            # Try to open the file or directory to check if it's locked or being used by another user
            if os.path.isfile(self.path):
                try:
                    with open(self.path, 'r') as f:
                        pass
                except IOError:
                    raise IOError(f"File cannot be opened: {self.path}")
        except Exception as e:
            print(f"Error validating file path: {e}")
            return False
        return True

    def validate_path(self):
        while not (self.__is_valid_path_or_dir()):
            self.path = input("Enter valid path or directory: ")
        return self.path


class TargetDirectoryValidator:
    def __init__(self, target_directory):
        self.target_directory = target_directory

    def __is_valid_target_directory(self):
        try:
            if self.target_directory.startswith(
                    '"') and self.target_directory.endswith('"'):
                self.target_directory = self.target_directory.strip('""')
            if not os.path.exists(self.target_directory):
                raise FileNotFoundError(
                    f"Directory not found: {self.target_directory}")
        except Exception as e:
            print(f"Error validating target directory: {e}")
            return False
        return True

    def validate_target_directory_input(self):
        while not self.__is_valid_target_directory():
            self.target_directory = input("Enter a valid target directory: ")
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
