import json
import os
from compression_init import CompressorInit as Ci


class AddToArchive:
    def __init__(self, archive_path, archive_metadata,
                 archive_metadata_length,
                 target_dir):
        self.compressed_file_metadata = None
        self.compressed_file_content = None
        self.compressed_file_path = None
        self.added_file_path = None
        self.archive_path = archive_path
        self.archive_metadata = archive_metadata
        self.archive_metadata_length = archive_metadata_length
        self.target_dir = target_dir

    def archive_content_position(self, metadata_header):
        """
        Find the position of the archive content in the archive file.
        :param metadata_header:
        :return:
        """
        with open(self.archive_path, 'rb') as f:
            sequence = bytearray()
            while f.tell() > 0:  # While not at the start of the file
                f.seek(-1, os.SEEK_CUR)  # Move the pointer back 1 byte
                byte = f.read(1)  # Read the byte
                sequence.insert(0, byte[
                    0])  # Add the byte to the start of the found sequence
                if len(sequence) > len(
                        metadata_header):  # If the found sequence is too long
                    sequence.pop()  # Remove the last byte
                    # If the found sequence matches the
                if sequence == metadata_header:
                    # target sequence
                    return f.tell()
                # Move the pointer back 1 byte again to correct for the read
                f.seek(-1, os.SEEK_CUR)
        return None  # Return None if the sequence was not found

    def add_file_content(self):
        try:
            metadata_header_position = self.archive_content_position(
                b'ZM\x01\x02')
            if metadata_header_position is not None:
                with open(self.archive_path, 'r+b') as f:
                    f.seek(metadata_header_position)
                    # Write the new content
                    f.write(self.compressed_file_content + self.archive_metadata)
            else:
                raise ValueError("Metadata header missing in archive.")
        except ValueError as e:
            print(f"Error: {e}")

    def find_largest_pointer(self):
        largest_pointer = 0
        for key, value in self.archive_metadata.items():
            if isinstance(value, dict):
                if value["pointer"] > largest_pointer:
                    largest_pointer = value["pointer"]
        return largest_pointer

    def update_file_pointers(self):
        largest_pointer = self.find_largest_pointer()
        for key, value in self.compressed_file_metadata.items():
            if isinstance(value, dict):
                if isinstance(value["pointer"], int):
                    value["pointer"] += largest_pointer

    def process_file_metadata(self, file_metadata):
        file_metadata = file_metadata.decode('utf-8')
        self.compressed_file_metadata = json.loads(file_metadata)
        self.update_file_pointers()

    def join_metadata(self, file_metadata):
        self.process_file_metadata(file_metadata)
        self.archive_metadata.update(self.compressed_file_metadata)
        self.archive_metadata = json.dumps(self.archive_metadata)
        self.archive_metadata = self.archive_metadata.encode('utf-8')

    def add_file_to_archive(self):
        self.added_file_path = Ci.get_path()
        c = Ci(self.target_dir, self.added_file_path)
        # following step returns the encoded_content, metadata
        compressed_file_data = c.compressor_init_main()
        self.compressed_file_path = compressed_file_data[0]
        os.remove(self.compressed_file_path)
        self.compressed_file_content = compressed_file_data[1]
        self.join_metadata(compressed_file_data[2])
        self.add_file_content()
