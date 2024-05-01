from pathlib import Path
import struct
import os
from helper_functions import hash_data
from config import MAX_COUNT


class RunLengthEncoder:

    def __init__(self, path, unit_length):
        self.path = path
        self.file_name = Path(path).stem
        self.unit_length = unit_length
        self.content = self.open_file()
        self.bytes_num = os.path.getsize(self.path)

    def open_file(self):
        with open(self.path, 'rb') as f:
            content = f.read()
        return content

    def content_encoder(self, header):
        encoded = [header]
        count = 1
        encoded_content_size = 0

        if self.unit_length >= self.bytes_num:
            encoded.append(struct.pack('B', 1) + self.content)
            encoded = b''.join(encoded)
            encoded_content_size = len(encoded)
            return encoded, encoded_content_size

        curr_unit = self.content[0:self.unit_length]
        for i in range(self.unit_length, self.bytes_num, self.unit_length):
            if i + self.unit_length > self.bytes_num:
                next_unit = self.content[i:]
            else:
                next_unit = self.content[i:i + self.unit_length]

            if curr_unit == next_unit:
                count += 1
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

        encoded_unit = struct.pack('B', count) + curr_unit
        encoded.append(encoded_unit)
        encoded_content_size += len(encoded_unit)

        return b''.join(encoded), encoded_content_size

    def rle_encode(self):
        hashed_content = hash_data(self.content)
        encoded, encoded_content_size = self.content_encoder(hashed_content)

        return encoded, encoded_content_size, str(hashed_content), self.bytes_num



