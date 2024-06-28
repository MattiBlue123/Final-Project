from encoder import RunLengthEncoder
from archive import ArchiveCreator
from config import FILE_HEADER_LENGTH
from compression_info import (file_compressing_timer_decorator,
                              archiving_timer_decorator)


class Compressor:
    """
    The Compressor class is responsible for
    compressing files using Run Length Encoding.
    """

    def __init__(self, metadata, target_dir, archive_name):
        """
        Initialize the Compressor with metadata,
         target directory, and archive name.
        """
        self.metadata = metadata
        self.target_dir = target_dir
        self.archive_name = archive_name
        self.original_data_size = 0

    @file_compressing_timer_decorator
    def file_compressor(self, metadata, pointer=0):
        """
        Compress a single file using Run Length Encoding.
        """
        # initialize the RunLengthEncoder with the file path and unit length
        encoder = RunLengthEncoder(metadata.pop("origin path"),
                                   metadata["unit length"])
        # encode the content of the file, returns encoded content,
        # encoded_content_size, original size
        rle_return_vals = encoder.rle_encode()
        encoded_content = rle_return_vals[0]
        metadata["pointer"] = rle_return_vals[1] + FILE_HEADER_LENGTH + pointer
        # update the metadata with the original and encoded sizes
        metadata = self.update_metadata(metadata, *rle_return_vals[1:])
        return metadata, encoded_content, metadata["pointer"]

    def compress_all_files(self, metadata, all_encoded_content_list,
                           general_pointer=0):
        """
        Compress all files in the metadata dictionary.
        It uses recursion to compress files in folders.
        Due to runtime limitations of the function, it uses a list to append
        the encoded content of each file and then compress() joins them.
        """
        for key, value in metadata.items():
            # if the value is a dict, it means that we are now looking at a
            # file or a folder. still need to check the type.
            if isinstance(value, dict):

                if value["type"] == "file":
                    (metadata[key], encoded_content, general_pointer) = \
                        self.file_compressor(metadata[key], general_pointer)

                    all_encoded_content_list.append(encoded_content)

                elif value["type"] == "folder":
                    (metadata[key],
                     all_encoded_content_list,
                     general_pointer) = \
                        self.compress_all_files(value,
                                                all_encoded_content_list,
                                                general_pointer)

        return metadata, all_encoded_content_list, general_pointer

    def update_metadata(self, file_metadata, encoded_content_size, bytes_num):
        """
        Update the metadata dictionary with the original and encoded sizes.
        """
        file_metadata["original size"] = bytes_num
        file_metadata["encoded size"] = encoded_content_size
        self.original_data_size += bytes_num
        return file_metadata

    @archiving_timer_decorator
    def compress(self, add_flag=False):
        """
        Compress all files and create an archive.
        """
        metadata, encoded_content, end_pointer = self.compress_all_files(
            self.metadata, [])

        encoded_content = b''.join(encoded_content)
        # archiving all the content
        archive = ArchiveCreator(metadata, encoded_content, end_pointer,
                                 self.target_dir, self.archive_name,
                                 self.original_data_size, add_flag)

        return archive.create_archive()
