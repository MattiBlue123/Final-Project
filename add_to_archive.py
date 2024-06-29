import os
from typing import Dict

from compression_init import CompressorInit as Ci
# from eval_string_to_dict import EvalStringToDict
import ast

from config import METADATA_FOOTER, METADATA_HEADER


class AddToArchive:
    """
    Responsible for adding a file to an existing archive.
    :param archive_path: The path to the archive file.
    :param archive_metadata: The metadata of the archive.
    Both parameters ar from the WorkOnArchive class.
    """

    def __init__(self, archive_path: str, archive_metadata: Dict):
        self.compressed_file_metadata = None
        self.compressed_file_content = None
        self.compressed_file_path = None
        self.added_file_path = None
        self.archive_path = archive_path
        self.archive_metadata = archive_metadata

    def find_largest_pointer(self, metadata_dict: Dict = None,
                             largest_pointer: int = 0) -> int:
        """
        Find the largest pointer in the metadata.
        This method is essential for updating the pointers of the new file
        that's being added to the archive.
        :param:
        metadata_dict (Dict): The metadata dictionary to search.
        largest_pointer (int): The largest pointer found.
        :return:
        int: The largest pointer found.
        """
        if metadata_dict is None:
            metadata_dict = self.archive_metadata
        # iterate through the metadata, if a pointer is found, check if it's
        # the larger than the ones found before.
        for key, value in metadata_dict.items():
            if isinstance(value, dict):
                if ("pointer" in value.keys() and
                        isinstance(value["pointer"], int)):
                    if value["pointer"] > largest_pointer:
                        largest_pointer = value["pointer"]
                largest_pointer = self.find_largest_pointer(value,
                                                            largest_pointer)

        return largest_pointer

    def update_file_pointers(self, metadata_dict: Dict = None,
                             largest_pointer: int = 0) -> None:
        """
        Update the pointers of the file added to the archive,
         to the largest pointer + the original file pointer.
         This method is good for a single file or a batch of files.
        :param:
        metadata_dict (Dict): The metadata dictionary to update.
        largest_pointer (int): The largest pointer found.
        :return:
        None
        """
        if metadata_dict is None:
            metadata_dict = self.compressed_file_metadata
            largest_pointer = self.find_largest_pointer()

        for key, value in metadata_dict.items():
            if isinstance(value, dict):
                if ("pointer" in value.keys() and
                        isinstance(value["pointer"], int)):
                    value["pointer"] += largest_pointer
                self.update_file_pointers(value, largest_pointer)

    def process_file_metadata(self) -> None:
        """
        Processes the metadata of the file to be added to the archive.
        :return:
        """
        # the metadata is in binary. Decode it to string.
        decoded_file_metadata = self.compressed_file_metadata.decode('utf-8')
        # convert the string to a metadata dictionary.
        self.compressed_file_metadata = ast.literal_eval(decoded_file_metadata)
        self.update_file_pointers()

    def join_metadata(self) -> None:
        """
        Join the metadata of the archive and the metadata of the new file/s.
        ncode the metadata to bytes to b added to the whole archive content
        :return:
        None
        """
        self.archive_metadata.update(self.compressed_file_metadata)
        self.archive_metadata = str(self.archive_metadata)
        self.archive_metadata = self.archive_metadata.encode('utf-8')

    def add_file_content(self, metadata_length: int = 0) -> None:
        """
        Add the content of the file to the archive.

        :param:
        metadata_length (int): The length of the metadata.
        :return:
        None
        """
        try:
            with open(self.archive_path, 'rb+') as f:
                print(f"Reading metadata from {self.archive_path}")
                f.seek(-4, os.SEEK_END)
                footer = f.read()

                if footer != METADATA_FOOTER:
                    raise ValueError(
                        "Invalid archive, missing appropriate footer")

                is_header = bytearray()

                while f.tell() > 0:  # While not at the start of the file
                    f.seek(-1, os.SEEK_CUR)  # Move the pointer back 1 byte
                    byte = f.read(1)  # Read the byte
                    is_header.insert(0, byte[
                        0])  # Add the byte to the start of the found sequence
                    metadata_length += 1  # Increment the header_length
                    if len(is_header) > 4:  # If the found sequence is too long
                        is_header.pop()  # Remove the last byte
                        # If the found sequence matches the target sequence
                    if is_header == METADATA_HEADER:
                        f.seek(-1, os.SEEK_CUR)
                        f.write(self.compressed_file_content)
                        f.write(METADATA_HEADER)
                        self.join_metadata()
                        # now the metadata is updated with the new file's
                        # it's a binary string by now
                        f.write(self.archive_metadata)
                        f.write(METADATA_FOOTER)
                        break

                    f.seek(-1, os.SEEK_CUR)

        except ValueError:
            raise ValueError("Metadata header missing in archive.")

    def add_file_to_archive(self) -> None:
        """
        This is the main method that adds the file to the archive,
        by calling th helper methods in this module
        :return:
        None
        """
        # get the path of the file to be added to the archive
        self.added_file_path = Ci.get_path(True)
        # init the compressor
        c = Ci(self.archive_path, self.added_file_path, True)
        # following step returns the encoded_content ([0]), metadata ([1])
        compressed_file_data = c.compressor_init_main()
        self.compressed_file_content = compressed_file_data[0]
        self.compressed_file_metadata = compressed_file_data[1]
        # the function is processioning the metadata to be added to the archive
        self.process_file_metadata()
        self.add_file_content()
        print("File added to archive successfully.")
