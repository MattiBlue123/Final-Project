import os
from typing import Dict

from decoder import RunLengthDecoder


class Decompressor:
    """
    The Decompressor class is responsible for decompressing an archive that
    was compressed using Run Length Encoding.
    """

    def __init__(self, path_to_archive: str, target_dir: str, metadata: Dict):
        """
        Initialize the Decompressor with the path to the archive, the target
        directory, the metadata of the files in the archive, and the length
        of the metadata.

        :param:
        path_to_archive (str): The path to the archive.
        target_dir (str): The target directory for the extracted files.
        metadata (dict): The metadata of the files in the archive.
        """
        self.path_to_archive = path_to_archive
        self.target_dir = target_dir
        self.metadata = metadata

    def extract_file(self, file_metadata: Dict, file_name: str,
                     target_dir: str) -> None:
        """
        Extract a file from the archive.

        :param:
        file_metadata (dict): The metadata of the file.
        file_name (str): The name of the file.
        target_dir (str): The directory where the extracted file will be saved.
        :return:
        None
        """
        # Create a RunLengthDecoder instance for the file
        decoder = RunLengthDecoder(file_metadata, file_name, target_dir,
                                   self.path_to_archive)
        # Decode and extract the file
        decoder.decode_file_to_extract()

    def extract_all_files(self, directory_metadata: Dict, target_dir: str) \
            -> None:
        """
        Extract all files from a directory in the archive.

        :param:
        directory_metadata (dict): The metadata of the directory.
        target_dir (str): The directory where the extracted files will be saved.
        :return:
        None
        """
        # Iterate over all items in the directory
        for key, value in directory_metadata.items():
            # If the value is a dictionary, it's a directory or a file
            if isinstance(value, dict):
                if value["type"] == "folder":
                    # If it's a directory, create a corresponding directory
                    # in the target directory
                    directory_path = os.path.join(target_dir, key)
                    os.mkdir(directory_path)
                    # Recursively extract all files in the directory
                    self.extract_all_files(value, directory_path)
                elif value["type"] == "file":
                    # If it's a file, extract the file
                    try:
                        self.extract_file(value, key, target_dir)
                    except ValueError as e:
                        print(f"Error extracting file {key}: {e}")
                        continue

    def extract(self) -> None:
        """
        Extract all files from the archive.
        """
        # Extract all files in the root directory of the archive
        self.extract_all_files(self.metadata, self.target_dir)
