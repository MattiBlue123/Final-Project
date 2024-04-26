import json

from encoder_update import RunLengthEncoder
import os


class Compressor:

    def __init__(self, metadata, target_dir, archive_name):
        self.metadata = metadata
        self.target_dir = target_dir
        self.archive_name = archive_name

    def file_compressor(self, metadata):
        encoder = RunLengthEncoder(metadata["origin path"],
                                   metadata["unit length"],
                                   metadata["path in archive"])
        rle_return_vals = encoder.encode()
        encoded_content = rle_return_vals[0]
        metadata = self.update_metadata(metadata, *rle_return_vals[1:])
        return metadata, encoded_content, metadata["pointer"]

    def compress_all_files(self, metadata,
                           encoded_content=b'', pointer=0):
        if not any(isinstance(value, dict) for value in metadata.values()):
            return self.file_compressor(metadata)

        for key, value in metadata.items():
            if isinstance(value, dict):
                # Check if it's a file's metadata
                if "origin path" in value:
                    # metadata[key], encoded_content, pointer =\
                    #     self.file_compressor(value)
                    metadata[
                        key], encoded_content, pointer = self.file_compressor(
                        metadata[key])
                else:
                    metadata[key], encoded_content, pointer =\
                        self.compress_all_files(value, encoded_content, pointer)

        return metadata, encoded_content, pointer

    def update_metadata(self, file_metadata, header_length,
                        encoded_content_size, hashed_content, bytes_num):
        # encoded, header_length, encoded_size, hashed_content, original_size
        file_metadata["original size"] = bytes_num
        file_metadata["header length"] = header_length
        file_metadata["encoded size"] = encoded_content_size
        file_metadata["pointer"] = header_length + encoded_content_size
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
            self.metadata)
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
            archive_name = f"{self.archive_name}_rle_compressed{suffix}.bin"
            archive_path = os.path.join(self.target_dir, archive_name)

            if not os.path.exists(archive_path):
                break
            counter = 1 if counter is None else counter + 1

        with open(archive_path, 'wb') as archive:
            archive.write(self.encoded_content)
        print(f"Archive created and saved to: {archive_path}")
