import struct
import os
from helper_functions import hash_data, make_unique_path
from config import FILE_HEADER_LENGTH
import ast

class RunLengthDecoder:

    def __init__(self, file_metadata, file_name, target_dir, path_to_archive):
        self.file_metadata = file_metadata
        self.file_name = file_name
        self.target_dir = target_dir
        self.path_to_archive = path_to_archive
        self.pointer = self.file_metadata["pointer"]
        self.encoded_size = self.file_metadata["encoded size"]
        self.unit_length = self.file_metadata["unit length"]
        self.data_hash = self.file_metadata["data hash"]
        self.original_size = self.file_metadata["original size"]
        self.decoded_content = b''
        self.decoded_size = 0


    def get_appearances_num(self, content, extra_bytes):
        es = self.encoded_size
        content_slice = content[es - extra_bytes:es - extra_bytes + 1]
        unpacked_content = struct.unpack('B', content_slice)
        return unpacked_content[0]

    def read_and_prepare_content(self):
        """
        This method reads the content from the archive file and prepares it for decoding.
        It also calculates the number of extra bytes if the encoded size is not a multiple of the unit length.

        Returns:
            tuple: A tuple containing the content read from the file and the number of extra bytes.
        """
        try:
            with open(self.path_to_archive, 'rb') as f:
                f.seek(self.pointer)
                f.seek(-self.encoded_size, os.SEEK_CUR)
                content = f.read(self.encoded_size)
                extra_bytes = 0
                if self.encoded_size % (self.unit_length + 1) != 0:
                    extra_bytes = self.encoded_size % (self.unit_length + 1)
            return content, extra_bytes
        except ValueError as e:
            raise ValueError(f"Error - wrong pointer for {self.file_name}:"
                             f" {e}")

    def decode_content(self, content, extra_bytes):
        """
        This method decodes the content read from the archive file.
        It unpacks the appearances number and the unit from the content and appends them to the decoded content parts.

        Args:
            content (bytes): The content read from the file.
            extra_bytes (int): The number of extra bytes.
        """
        decoded_content_parts = []
        for i in range(0, self.encoded_size - extra_bytes,
                       self.unit_length + 1):
            appearances_num = struct.unpack('B', content[i:i + 1])[0]
            unit = content[i + 1:i + self.unit_length + 1]
            decoded_unit = unit * appearances_num
            decoded_content_parts.append(decoded_unit)
            self.decoded_size += len(decoded_unit)

        if self.encoded_size % (self.unit_length + 1) != 0:
            appearances_num = self.get_appearances_num(content, extra_bytes)
            unit = content[self.encoded_size - extra_bytes + 1:]
            decoded_unit = unit * appearances_num
            decoded_content_parts.append(decoded_unit)
            self.decoded_size += len(decoded_unit)

        self.decoded_content = b''.join(decoded_content_parts)


    def validate_decoding_process(self):
        # validate the decoding process
        after_decoding_hash = hash_data(self.decoded_content)
        original_data_hash = ast.literal_eval(self.data_hash)
        if original_data_hash != after_decoding_hash:
            raise ValueError(f" Data corrupted - hash mismatch")
        if self.original_size != self.decoded_size:
            raise ValueError(f" Data corrupted -"
                             f" content has changed")

    def _is_text(self):
        # Try to decode a portion of the content as text
        try:
            self.decoded_content[:1024].decode('utf-8')
            return True  # is text
        except UnicodeDecodeError:
            return False  # is not text

    def decode_file_to_extract(self):
        try:
            content, extra_bytes = self.read_and_prepare_content()
            self.decode_content(content, extra_bytes)
            self.validate_decoding_process()
        except Exception as e:
            print(f"Error decoding {self.file_name}:  {e}")
            return
        is_text = self._is_text()
        # Open the file in the appropriate mode
        mode = 'w' if is_text else 'wb'
        extracted_file_path = make_unique_path(self.target_dir, self.file_name)
        with open(os.path.join(extracted_file_path), mode) as f:
            if is_text:
                f.write(self.decoded_content.decode('utf-8'))
            else:
                f.write(self.decoded_content)

            print(f"Extracted: {self.file_name}"
                  f" to the target directory: {self.target_dir}")
