import os
from decoder import RunLengthDecoder


class Decompressor:

    def __init__(self, path_to_archive, target_dir, metadata, metadata_length):
        self.path_to_archive = path_to_archive
        self.target_dir = target_dir
        self.metadata = metadata
        self.metadata_length = metadata_length

    def extract_file(self, file_metadata, file_name, target_dir):
        decoder = RunLengthDecoder(file_metadata, file_name, target_dir,
                                   self.path_to_archive)
        decoder.decode_file_to_extract()


    def extract_all_files(self, directory_metadata, target_dir):
        for key, value in directory_metadata.items():
            if isinstance(value, dict):
                if value["type"] == "folder":
                    directory_path = os.path.join(target_dir, key)
                    os.mkdir(directory_path)
                    self.extract_all_files(value, directory_path)
                elif value["type"] == "file":
                    self.extract_file(value, key, target_dir)

    def extract(self):
        # extract all files
        self.extract_all_files(self.metadata, self.target_dir)
