import json
from encoder import RunLengthEncoder
import os
from config import FLAGS


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

    # def compress_all_files(self, metadata, encoded_content=b'', pointer=0):
    #     print(f"metadata now is: \n {metadata}")
    #     for key, value in metadata.items():
    #         if isinstance(value, dict):
    #             # Check if it's a file's metadata
    #             if value["type"] == "file":
    #                 print(f"compressing file {key}")
    #                 print(f"metadata[key]: \n {metadata[key]}")
    #                 (metadata[key],
    #                  encoded_content,
    #                  pointer) = self.file_compressor(metadata[key])
    #
    #                 print(f"now metadata updated to: \n {metadata[key]}")
    #                 print(f"encoded content updated to: \n {encoded_content}")
    #                 print(f"pointer updated to: \n {pointer}")
    #             else:
    #                 metadata[key], encoded_content, pointer = \
    #                     self.compress_all_files(value, encoded_content,
    #                                             pointer)
    #
    #     return metadata, encoded_content, pointer
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
        # encoded, header_length, encoded_size, hashed_content, original_size
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


class ArchiveCreator:
    """The Archive class is responsible for creating a compressed archive of
    the files in the target directory. The archive is created in the target."""

    def __init__(self, metadata, encoded_content, pointer, target_dir,
                 archive_name):
        self.metadata = metadata
        self.encoded_content = encoded_content
        self.pointer = pointer
        self.target_dir = target_dir
        self.archive_name = archive_name

    def process_metadata(self):
        """
        Process the metadata for JSON serialization.

        Returns:
        bytes: The processed metadata.
        """
        # Convert metadata to JSON and encode to bytes
        self.metadata = json.dumps(self.metadata)
        self.metadata = self.metadata.encode('utf-8')

        # Add header and footer to the metadata
        header = b'ZM\x01\x02'
        footer = b'ZM\x05\x06'
        return header + self.metadata + footer

    def create_archive(self):
        # Create an archive of the compressed files
        self.encoded_content = self.encoded_content + self.process_metadata()
        # naming the archive file
        # making sure there isn't an existing file with the same name.
        # adding a number to the name if there is.
        counter = None
        while True:
            suffix = f"({counter})" if counter is not None else ""
            archive_name = f"{self.archive_name}_rle{suffix}"
            archive_path = os.path.join(self.target_dir, archive_name)

            if not os.path.exists(archive_path):
                break
            counter = 1 if counter is None else counter + 1

        with open(archive_path, 'wb') as archive:
            archive.write(self.encoded_content)
        print(f"Archive created and saved to: {archive_path}")
        FLAGS["back flag"] = True
