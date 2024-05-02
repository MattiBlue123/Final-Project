from encoder import RunLengthEncoder
from archive import ArchiveCreator
from config import FILE_HEADER_LENGTH
from compression_info import file_compressing_timer_decorator, archiving_timer_decorator


class Compressor:

    def __init__(self, metadata, target_dir, archive_name):
        self.metadata = metadata
        self.target_dir = target_dir
        self.archive_name = archive_name

    @file_compressing_timer_decorator
    def file_compressor(self, metadata, pointer=0):
        encoder = RunLengthEncoder(metadata.pop("origin path"),
                                   metadata["unit length"])
        rle_return_vals = encoder.rle_encode()
        encoded_content = rle_return_vals[0]
        metadata["pointer"] = rle_return_vals[1] + FILE_HEADER_LENGTH + pointer
        metadata = self.update_metadata(metadata, *rle_return_vals[1:])
        return metadata, encoded_content, metadata["pointer"]

    def compress_all_files(self, metadata, all_encoded_content_list,
                           general_pointer=0):

        for key, value in metadata.items():
            if isinstance(value, dict):
                # Check if it's a file's metadata
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

    @staticmethod
    def update_metadata(file_metadata, encoded_content_size, bytes_num):
        file_metadata["original size"] = bytes_num
        file_metadata["encoded size"] = encoded_content_size
        return file_metadata

    @archiving_timer_decorator
    def compress(self, add_flag=False):
        metadata, encoded_content, end_pointer = self.compress_all_files(
            self.metadata, [])
        encoded_content = b''.join(encoded_content)
        archive = ArchiveCreator(metadata, encoded_content, end_pointer,
                                 self.target_dir, self.archive_name, add_flag)

        return archive.create_archive()


