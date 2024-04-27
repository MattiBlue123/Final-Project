import os
from compression import Compressor
from config import CI_PROMPTS
from helper_functions import zinput, create_metadata
from validator import (PathValidator as Pv, TargetDirectoryValidator as TdV,
                       UnitLengthValidator as UlV)


class CompressorInit:

    def __init__(self):
        self.metadata = {}
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

    def compressor_init_main(self):
        metadata = dict()
        print(CI_PROMPTS["chelp"])  # will need to update this
        self.set_def_unit_length()
        path = self.get_path()
        self.archive_name = os.path.basename(path)
        if not self.unit_length:
            unit_length = self.get_unit_length()
        else:
            unit_length = self.unit_length
        metadata[self.archive_name] = create_metadata(path, unit_length,
                                                      self.archive_name)
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
                metadata[path_name] = create_metadata(path, unit_length,
                                                      path_name)
        compressor = Compressor(metadata, self.target_dir, self.archive_name)
        compressor.compress()
