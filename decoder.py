from pathlib import Path
import struct
import os
from helper_functions import hash_data


class RunLengthDecoder:

    def __init__(self, file_metadata, file_name, target_dir, path_to_archive):
        self.file_metadata = file_metadata
        self.file_name = file_name
        self.target_dir = target_dir
        self.path_to_archive = path_to_archive
        self.pointer = self.file_metadata["pointer"]
        self.header_length = self.file_metadata["header length"]
        self.encoded_size = self.file_metadata["encoded size"]
        self.unit_length = self.file_metadata["unit length"]
        self.data_hash = self.file_metadata["data hash"]
        self.original_size = self.file_metadata["original size"]
        self.decoded_content = b''
        self.path_in_archive = self.file_metadata["path in archive"]

    def content_decoder(self, header):



    def encode(self):
        hashed_content = hash_data(self.content)
        hashed_content = str(hashed_content)
        header = hash_data(self.path_in_archive.encode('utf-8'))
        encoded, encoded_content_size = self.content_encoder(header)

        return encoded, len(
            header), encoded_content_size, hashed_content, self.bytes_num

    def validate_header(self, file_header):
        # validate the header
        if file_header != hash_data(self.path_in_archive.encode('utf-8')):
            raise ValueError("Invalid header")
    def validate_decoding_process(self):
        # validate the decoding process
        if self.data_hash != hash_data(self.content):
            raise ValueError("Data corrupted")
        if self.original_size != len(self.content):
            raise ValueError("Data corrupted")