import os
from compression import Compressor
from config import CI_PROMPTS
from helper_functions import zinput
from validator import (PathValidator as Pv, TargetDirectoryValidator as TdV,
                       UnitLengthValidator as UlV)


class CompressorInit:

    def __init__(self):
        self.metadata = dict()
        self.target_dir = ''
        self.unit_length = 0
        self.archive_name = ''

    def set_def_unit_length(self):
        unit_length = zinput(CI_PROMPTS["set default unit length"]).strip()
        unit_length = UlV(unit_length).validate_unit_length()
        if unit_length:
            self.unit_length = unit_length

    @staticmethod
    def get_path():
        path = Pv(zinput(CI_PROMPTS["get path"]).strip('""')).validate_path()
        return path

    @staticmethod
    def get_unit_length():
        unit_length = UlV(zinput(
            CI_PROMPTS["get ul"]).strip()).validate_unit_length()
        return unit_length

    def get_target_dir(self):
        target_dir = zinput("Please enter the target directory: ").strip('""')
        self.target_dir = TdV(target_dir).validate_target_directory()

    def create_file_metadata(self, path, unit_length, path_in_archive):
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

    def create_directory_metadata(self, path, unit_length, path_in_archive):
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
                    file_path, unit_length, path_in_archive + "/" + file)
            else:
                directory_metadata[file] = self.create_file_metadata(
                    file_path, unit_length, path_in_archive + "/" + file)
        return directory_metadata

    def create_metadata(self, path, unit_length, path_in_archive=""):
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
            return self.create_directory_metadata(path, unit_length,
                                                  path_in_archive)
        else:
            return self.create_file_metadata(path, unit_length,
                                             path_in_archive)

    def compressor_init_main(self):
        print(CI_PROMPTS["chelp"])  # will need to update this
        self.set_def_unit_length()
        path = self.get_path()
        self.archive_name = os.path.basename(path)
        if not self.unit_length:
            unit_length = self.get_unit_length()
        else:
            unit_length = self.unit_length
        self.metadata[self.archive_name] =\
            self.create_metadata(path, unit_length, self.archive_name)
        self.get_target_dir()
        while True:
            path = zinput(
                CI_PROMPTS["another path"]).strip('""')
            if path.lower() == 'ok':
                break
            else:
                # validate the paths
                path = Pv(path).validate_path()
                if not self.unit_length:
                    unit_length = self.get_unit_length()
                else:
                    unit_length = self.unit_length
                path_name = os.path.basename(path)
                self.metadata[path_name] = self.create_metadata(path,
                                                                unit_length,
                                                                path_name)
        compressor = Compressor(self.metadata, self.target_dir,
                                self.archive_name)
        compressor.compress()
