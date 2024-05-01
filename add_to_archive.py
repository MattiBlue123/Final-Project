import json
import os
from compression_init import CompressorInit as Ci


class AddToArchive:
    def __init__(self, archive_path, archive_metadata):
        self.compressed_file_metadata = None
        self.compressed_file_content = None
        self.compressed_file_path = None
        self.added_file_path = None
        self.archive_path = archive_path
        self.archive_metadata = archive_metadata

    def find_largest_pointer(self, metadata_dict=None, largest_pointer=0):
        if metadata_dict is None:
            metadata_dict = self.archive_metadata

        for key, value in metadata_dict.items():
            if isinstance(value, dict):
                if "pointer" in value.keys() and isinstance(value["pointer"],
                                                            int):
                    if value["pointer"] > largest_pointer:
                        largest_pointer = value["pointer"]
                largest_pointer = self.find_largest_pointer(value,
                                                            largest_pointer)

        return largest_pointer

    def update_file_pointers(self, metadata_dict=None, largest_pointer=0):
        if metadata_dict is None:
            metadata_dict = self.compressed_file_metadata
            largest_pointer = self.find_largest_pointer()

        for key, value in metadata_dict.items():
            if isinstance(value, dict):
                if "pointer" in value.keys() and isinstance(value["pointer"],
                                                            int):
                    value["pointer"] += largest_pointer
                self.update_file_pointers(value, largest_pointer)


    def process_file_metadata(self):
        self.compressed_file_metadata = self.compressed_file_metadata.decode('utf-8')
        self.compressed_file_metadata = json.loads(self.compressed_file_metadata)
        self.update_file_pointers()

    def join_metadata(self):
        self.archive_metadata.update(self.compressed_file_metadata)
        self.archive_metadata = json.dumps(self.archive_metadata)
        self.archive_metadata = self.archive_metadata.encode('utf-8')

    def add_file_content(self, metadata_length=0):
        try:
            with open(self.archive_path, 'rb+') as f:
                print(f"Reading metadata from {self.archive_path}")
                f.seek(-4, os.SEEK_END)
                footer = f.read()

                if footer != b'ZM\x05\x06':
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
                    if is_header == b'ZM\x01\x02':  # If the found sequence matches the target sequence
                        f.seek(-1, os.SEEK_CUR)
                        f.write(self.compressed_file_content)
                        f.write(b'ZM\x01\x02')
                        self.join_metadata()
                        f.write(self.archive_metadata)
                        f.write(b'ZM\x05\x06')
                        break

                    f.seek(-1, os.SEEK_CUR)

        except ValueError:
            raise ValueError("Metadata header missing in archive.")




    def add_file_to_archive(self):
        # get the path of the file to be added to the archive
        self.added_file_path = Ci.get_path(True)
        # init the compressor
        c = Ci(self.archive_path, self.added_file_path, True)
        # following step returns the encoded_content, metadata
        compressed_file_data = c.compressor_init_main()
        self.compressed_file_content = compressed_file_data[0]
        self.compressed_file_metadata = compressed_file_data[1]
        self.process_file_metadata()
        self.add_file_content()
        print("File added to archive successfully.")

