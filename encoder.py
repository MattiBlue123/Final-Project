from pathlib import Path
import struct
import os
from helper_functions import hash_data
from config import MAX_COUNT


class RunLengthEncoder:
    """
    The RunLengthEncoder class is responsible for encoding
    a file using Run Length Encoding.
    """

    def __init__(self, path, unit_length):
        """
        Initialize the RunLengthEncoder with the path of the file to
        be encoded and the unit length.

        :param path: The path of the file to be encoded.
        :param unit_length: The unit length for encoding.
        """
        self.path = path
        self.file_name = Path(path).stem
        self.unit_length = unit_length
        self.content = self.open_file()
        self.bytes_num = os.path.getsize(self.path)

    def open_file(self):
        """
        Open the file at the given path and read its content.

        :return: The content of the file.
        """
        with open(self.path, 'rb') as f:
            content = f.read()
        return content

    def content_encoder(self, header):
        """
        Encode the content of the file using Run Length Encoding.

        :param header: The header to be added to the encoded content.
        :return: The encoded content and its size.
        """
        encoded = [header]
        count = 1
        encoded_content_size = 0
        # if the unit length is greater than or equal
        # to the number of bytes in the content, don't need to encode it.
        if self.unit_length >= self.bytes_num:
            encoded.append(struct.pack('B', 1) + self.content)
            encoded = b''.join(encoded)
            encoded_content_size = len(encoded)
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

    def rle_encode(self):
        """
        Encode the content of the file using Run Length Encoding
        and return the encoded content, its size, and the original size.

        :return: The encoded content, its size, and the original size.
        """
        hashed_content = hash_data(self.content)
        encoded, encoded_content_size = self.content_encoder(hashed_content)

        return encoded, encoded_content_size, self.bytes_num
