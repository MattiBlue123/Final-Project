import os
from compression import Compressor
from config import CI_PROMPTS
from helper_functions import zinput
from validator import (PathValidator as Pv, TargetDirectoryValidator as TdV,
                       UnitLengthValidator as UlV)


class CompressorInit:

    def __init__(self, target_dir='', added_file_path=None, add_flag=False):
        self.metadata = dict()
        self.target_dir = target_dir
        self.unit_length = 0
        self.archive_name = ''
        self.added_file_path = added_file_path
        self.add_flag = add_flag

    def set_def_unit_length(self):
        unit_length = zinput(CI_PROMPTS["set default unit length"]).strip()
        unit_length = UlV(unit_length).validate_unit_length()
        if unit_length:
            self.unit_length = unit_length

    @staticmethod
    def get_path(first=False):
        if first:
            path = Pv(
                zinput(CI_PROMPTS["get path"]).strip('""')).validate_path()
            return path
        else:
            path = zinput(CI_PROMPTS["another path"]).strip('""')
            if path == 'ok':
                return 'ok'
            else:
                Pv(path).validate_path()
                return path

    @staticmethod
    def get_unit_length():
        unit_length = UlV(zinput(
            CI_PROMPTS["get ul"]).strip()).validate_unit_length()
        return unit_length

    def get_target_dir(self):
        target_dir = zinput("Please enter the target directory: ").strip('""')
        self.target_dir = TdV(target_dir).validate_target_directory()

    @staticmethod
    def create_file_metadata(path, unit_length):
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
        file_metadata["pointer"] = None
        file_metadata["encoded size"] = None
        file_metadata["unit length"] = unit_length
        file_metadata["data hash"] = None
        file_metadata["original size"] = os.path.getsize(path)
        return file_metadata

    def create_directory_metadata(self, path, unit_length):
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
                directory_metadata[file] = self.create_directory_metadata(
                    file_path, unit_length)
            else:
                directory_metadata[file] = self.create_file_metadata(
                    file_path, unit_length)
        return directory_metadata

    def create_metadata(self, path, unit_length):
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
            return self.create_directory_metadata(path, unit_length)
        else:
            return self.create_file_metadata(path, unit_length)

    def compressor_init_main(self):
        print(CI_PROMPTS["--chelp"])  # will need to update this
        self.set_def_unit_length()
        if not self.added_file_path:
            path = self.get_path(True)
        else:
            path = self.added_file_path
        self.archive_name = os.path.basename(path)
        if not self.unit_length:
            unit_length = self.get_unit_length()
        else:
            unit_length = self.unit_length
        self.metadata[self.archive_name] = \
            self.create_metadata(path, unit_length)
        if self.target_dir == '':
            self.get_target_dir()
        while True:
            path = self.get_path()
            if path == 'ok':
                break
            else:
                # validate the paths
                if not self.unit_length:
                    unit_length = self.get_unit_length()
                else:
                    unit_length = self.unit_length
                path_name = os.path.basename(path)
                self.metadata[path_name] = self.create_metadata(path,
                                                                unit_length)
        compressor = Compressor(self.metadata, self.target_dir,
                                self.archive_name)
        compressed_output = compressor.compress(self.add_flag)

        if compressed_output:
            return compressed_output
        else:
            return


