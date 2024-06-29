from pathlib import Path
import struct
import os
from typing import Tuple
from helper_functions import hash_data
from config import MAX_COUNT, FILE_HEADER_LENGTH


class RunLengthEncoder:
    """
    The RunLengthEncoder class is responsible for encoding
    a file using Run Length Encoding.
    """

    def __init__(self, path: str, unit_length: int):
        """
        Initialize the RunLengthEncoder with the path of the file to
        be encoded and the unit length.
        :param:
        path (str): The path of the file to be encoded.
        unit_length (int): The unit length for encoding.
        """
        self.path = path
        self.file_name = Path(path).stem
        self.unit_length = unit_length
        self.content = self.open_file()
        self.bytes_num = os.path.getsize(self.path)

    def open_file(self) -> bin:
        """
        Open the file at the given path and read its content.

        :return:
        content (bin): The content of the file.
        """
        with open(self.path, 'rb+') as f:
            content = f.read()
        if not content:
            return b' '
        return content

    def content_encoder(self, header: bytes) -> Tuple:
        """
        Encode the content of the file using Run Length Encoding.

        :param:
         header: The header to be added to the encoded content.
        :return:
         The encoded content and its size.
        """
        encoded = [header]
        count = 1
        encoded_content_size = 0
        # if the unit length is greater than or equal
        # to the number of bytes in the content, don't need to encode it.
        if self.unit_length > self.bytes_num:
            encoded.append(struct.pack('B', 1) + self.content)
            encoded = b''.join(encoded)
            encoded_content_size = len(encoded) - FILE_HEADER_LENGTH
            return encoded, encoded_content_size

        # encode the content
        curr_unit = self.content[0:self.unit_length]
        for i in range(self.unit_length, self.bytes_num, self.unit_length):
            if i + self.unit_length > self.bytes_num:
                next_unit = self.content[i:]
            else:
                next_unit = self.content[i:i + self.unit_length]

            # meaning its repeating
            if curr_unit == next_unit:
                count += 1
                # due to limitations in struct.pack,
                # we can only pack 255 at a time
                if count == MAX_COUNT + 1:
                    encoded_unit = struct.pack('B', MAX_COUNT) + curr_unit
                    encoded.append(encoded_unit)
                    encoded_content_size += len(encoded_unit)
                    count = 1
                    curr_unit = next_unit

            else:  # sequence of identical units ended
                encoded_unit = struct.pack('B', count) + curr_unit
                encoded.append(encoded_unit)
                encoded_content_size += len(encoded_unit)
                count = 1
                curr_unit = next_unit

        # for the last unit
        encoded_unit = struct.pack('B', count) + curr_unit
        encoded.append(encoded_unit)
        encoded_content_size += len(encoded_unit)

        return b''.join(encoded), encoded_content_size

    def rle_encode(self) -> Tuple[bin, int, int]:
        """
        Encode the content of the file using Run Length Encoding
        and return the encoded content, its size, and the original size.

        :return: The encoded content, its size, and the original size.
        """
        if not self.content:
            return b'', 0, self.bytes_num
        hashed_content = hash_data(self.content)
        encoded, encoded_content_size = self.content_encoder(hashed_content)

        return encoded, encoded_content_size, self.bytes_num
