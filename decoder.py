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
        # self.header = self.get_header()
        self.decoded_size = 0

    # def get_header(self):
    #     ### I have to fix this
    #     with open(self.path_to_archive, 'rb') as f:
    #         f.seek(self.pointer)
    #         header = f.read(self.header_length)
    #         header = header.decode('utf-8')
    #     return header

    def content_decoder(self):
        decoded_content_parts = []
        with open(self.path_to_archive, 'rb') as f:
            try:
                f.seek(self.pointer)
            except ValueError:
                pass
            try:
                f.seek(-self.encoded_size, os.SEEK_CUR)
            except ValueError:
                pass
            print(f"pointer: {f.tell()}")
            content = f.read(self.encoded_size)
            extra_bytes = 0
            if self.encoded_size % (self.unit_length + 1) != 0:
                extra_bytes = self.encoded_size % (self.unit_length + 1)

            for i in range(0, self.encoded_size - extra_bytes,
                           self.unit_length + 1):
                appearances_num = struct.unpack('B', content[i:i + 1])[0]
                unit = content[i + 1:i + self.unit_length + 1]
                decoded_content_parts.append(unit * appearances_num)

            if self.encoded_size % (self.unit_length + 1) != 0:
                appearances_num = struct.unpack('B', content[
                                                     self.encoded_size - extra_bytes:self.encoded_size - extra_bytes + 1])[
                    0]
                unit = content[self.encoded_size - extra_bytes + 1:]
                decoded_content_parts.append(unit * appearances_num)

        self.decoded_content = b''.join(decoded_content_parts)
    # def content_decoder(self):
    #
    #     print("Decoding content")
    #     with open(self.path_to_archive, 'rb') as f:
    #         print(f"Reading content from {self.file_name}")
    #         try:
    #             f.seek(self.pointer)
    #         except ValueError:
    #             print(f"Error seeking for pointer in {self.file_name}")
    #         try:
    #             f.seek(-self.encoded_size, os.SEEK_CUR)
    #         except ValueError:
    #             print(f"Error finding content beginning"
    #                   f" of {self.file_name}")
    #         content = f.read(self.encoded_size)
    #         print(f"Done reading content : {content}")  # working
    #         print(f"{self.encoded_size % (self.unit_length + 1) != 0}")
    #         extra_bytes = 0
    #         if self.encoded_size % (self.unit_length + 1) != 0:
    #             extra_bytes = self.encoded_size % (self.unit_length + 1)
    #         print(f"Extra bytes: {extra_bytes}")
    #
    #         for i in range(0, self.encoded_size - extra_bytes,
    #                        self.unit_length + 1):
    #             print("inside loop")
    #             appearances_num = struct.unpack('B', content[i:i + 1])[0]
    #             print(type(appearances_num), appearances_num)
    #             unit = content[i + 1:i + self.unit_length + 1]
    #             print(unit)
    #             self.decoded_content += unit * appearances_num
    #             print(self.decoded_content)
    #
    #         if self.encoded_size % (self.unit_length + 1) != 0:
    #             appearances_num = struct.unpack('B', content[
    #                                                  self.encoded_size -
    #                                                  extra_bytes:self.encoded_size - extra_bytes + 1])[
    #                 0]
    #
    #             unit = content[self.encoded_size - extra_bytes + 1:]
    #             self.decoded_content += unit * appearances_num

    # def validate_header(self):
    #     # validate the header
    #     #  the encoding of the file header was:
    #     #  header = hash_data(self.path_in_archive.encode('utf-8'))
    #     if self.file_header != hash_data(self.path_in_archive):
    #         raise ValueError(f"file {self.file_name} corrupted"
    #                          f" - file's header is not valid")

    def validate_decoding_process(self):
        # validate the decoding process
        if self.data_hash != hash_data(self.decoded_content):
            raise ValueError(f"{self.file_name}Data corrupted - hash mismatch")
        if self.original_size != self.decoded_size:
            raise ValueError(f"{self.file_name} Data corrupted -"
                             f" content has changed")

    def _is_text(self):
        # Try to decode a portion of the content as text
        try:
            self.decoded_content[:1024].decode('utf-8')
            return True  # is text
        except UnicodeDecodeError:
            return False  # is not text

    def extract(self):
        self.content_decoder()
        is_text = self._is_text()
        # Open the file in the appropriate mode
        mode = 'w' if is_text else 'wb'
        with open(os.path.join(self.target_dir, self.file_name), mode) as f:
            if is_text:
                f.write(self.decoded_content.decode('utf-8'))
            else:
                f.write(self.decoded_content)

        print(f"Extracted: {self.file_name}")
