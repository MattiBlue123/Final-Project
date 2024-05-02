import os
from decoder import RunLengthDecoder


class Decompressor:
    """
    The Decompressor class is responsible for decompressing an archive that
    was compressed using Run Length Encoding.
    """

    def __init__(self, path_to_archive, target_dir, metadata, metadata_length):
        """
        Initialize the Decompressor with the path to the archive, the target
        directory, the metadata of the files in the archive, and the length
        of the metadata.

        :param path_to_archive: The path to the archive to be decompressed.
        :param target_dir: The directory where the
         decompressed files will be saved.
        :param metadata: The metadata of the files in the archive.
        :param metadata_length: The length of the metadata.
        """
        self.path_to_archive = path_to_archive
        self.target_dir = target_dir
        self.metadata = metadata
        self.metadata_length = metadata_length

    def extract_file(self, file_metadata, file_name, target_dir):
        """
        Extract a file from the archive.

        :param file_metadata: The metadata of the file to be extracted.
        :param file_name: The name of the file.
        :param target_dir: The directory where the extracted file will be saved
        """
        # Create a RunLengthDecoder instance for the file
        decoder = RunLengthDecoder(file_metadata, file_name, target_dir,
                                   self.path_to_archive)
        # Decode and extract the file
        decoder.decode_file_to_extract()

    def extract_all_files(self, directory_metadata, target_dir):
        """
        Extract all files from a directory in the archive.

        :param directory_metadata: The metadata of the directory.
        :param target_dir: The directory where
         the extracted files will be saved.
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
                    self.extract_file(value, key, target_dir)

    def extract(self):
        """
        Extract all files from the archive.
        """
        # Extract all files in the root directory of the archive
        self.extract_all_files(self.metadata, self.target_dir)