import os
from decoder import RunLengthDecoder


class Decompressor:

    def __init__(self, path_to_archive, target_dir, metadata, metadata_length):
        self.path_to_archive = path_to_archive
        self.target_dir = target_dir
        self.metadata = metadata
        self.metadata_length = metadata_length

    def extract_file(self, file_metadata, file_name, target_dir):
        ("I've made it to the extract file method!")
        decoder = RunLengthDecoder(file_metadata, file_name, target_dir,
                                   self.path_to_archive)
        decoder.extract()

    def extract_all_files(self, directory_metadata, target_dir):
        print(f"init extract all files: {directory_metadata}\n"
              f" {target_dir}")
        for key, value in directory_metadata.items():
            if isinstance(value, dict):
                if value["type"] == "folder":
                    directory_path = os.path.join(target_dir, key)
                    os.mkdir(directory_path)
                    self.extract_all_files(value, directory_path)
                elif value["type"] == "file":
                    print(f"going to extract soon! {value}\n"
                          f" {key}\n"
                          f" {target_dir}")
                    self.extract_file(value, key, target_dir)

    def extract(self):
        try:
            # extract all files
            self.extract_all_files(self.metadata, self.target_dir)
        except Exception as e:
            print(f"Error extracting files: {self.path_to_archive}")
            return False
