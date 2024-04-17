import shutil
import os
import json
import base64
from compression import FileCompressor


class BatchCompressor:
    def __init__(self, file_paths, target_directory, unit_length):
        self.file_paths = file_paths
        self.target_directory = target_directory
        self.unit_length = unit_length

    def compress_files(self):
        compressed_files_dict = {}
        for file_path in self.file_paths:
            compressor = FileCompressor(file_path, self.target_directory,
                                        self.unit_length)
            compressed_content = compressor.compress_and_save()
            compressed_files_dict[
                os.path.basename(file_path)] = base64.b64encode(
                compressed_content).decode('utf-8')
        return compressed_files_dict

    def create_archive(self):
        compressed_files_dict = self.compress_files()
        with open(os.path.join(self.target_directory,
                               "compressed_files_dict.json"), 'w') as f:
            json.dump(compressed_files_dict, f)
        shutil.make_archive(
            os.path.join(self.target_directory, "compressed_files"), 'zip',
            self.target_directory, "compressed_files_dict.json")
