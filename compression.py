from encoder import RunLengthEncoder
from archive import ArchiveCreator

class Compressor:

    def __init__(self, metadata, target_dir, archive_name):
        self.metadata = metadata
        self.target_dir = target_dir
        self.archive_name = archive_name

    def file_compressor(self, metadata, pointer=0):
        encoder = RunLengthEncoder(metadata["origin path"],
                                   metadata["unit length"],
                                   metadata["path in archive"])
        rle_return_vals = encoder.encode()
        encoded_content = rle_return_vals[0]
        print(f"header length: {rle_return_vals[1]}")
        print(f"encoded size: {rle_return_vals[2]}")
        print(f"pointer before the file: {pointer}")
        metadata["pointer"] = rle_return_vals[1] + rle_return_vals[2] + pointer
        print(f"pointer after the file: {metadata['pointer']}")
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
                    print(f"general pointer updated to: {general_pointer}")

                elif value["type"] == "folder":
                    (metadata[key],
                     all_encoded_content_list,
                     general_pointer) = \
                        self.compress_all_files(value,
                                                all_encoded_content_list,
                                                general_pointer)

        return metadata, all_encoded_content_list, general_pointer

    def update_metadata(self, file_metadata, header_length,
                        encoded_content_size, hashed_content, bytes_num):
        file_metadata["original size"] = bytes_num
        file_metadata["header length"] = header_length
        file_metadata["encoded size"] = encoded_content_size
        file_metadata["data hash"] = hashed_content
        return file_metadata

    def compress(self):
        """
        Create metadata for a file or directory.

        Parameters:
        path (str): The path of the file or directory.
        unit_length (int): The unit length.
        path_in_archive (str): The path in the archive.

        Returns:
        dict: The metadata of the file or directory.
        """
        metadata, encoded_content, end_pointer = self.compress_all_files(
            self.metadata, [])
        encoded_content = b''.join(encoded_content)
        archive = ArchiveCreator(metadata, encoded_content, end_pointer,
                                 self.target_dir, self.archive_name)
        return archive.create_archive()


