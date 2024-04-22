from pathlib import Path
import struct
import os


class RunLengthEncoder:
    def __init__(self, file_path, unit_length, file_id):
        self.file_path = file_path
        self.file_name = Path(file_path).stem
        self.file_id = file_id
        self.unit_length = unit_length

    def encode(self):
        # open the file in binary mode

        # open_file(file_path)


        with open(self.file_path, 'rb') as f:
            content = f.read()
            encoded = self.file_id
            bytes_num = os.path.getsize(self.file_path)
            count = 1
            # the following line was added for the header
            # it's not len( content) in order to reduce runtime complexity
            encoded_content_size = 0

            if self.unit_length >= bytes_num:
                encoded = content
                return encoded
                # encode the content

            for i in range(0, bytes_num - (bytes_num % self.unit_length),
                           self.unit_length):
                # making sure next unit exists
                if i + self.unit_length >= bytes_num:
                    break
                curr_unit = content[i:i + self.unit_length]
                next_unit = content[
                            i + self.unit_length:i + 2 * self.unit_length]

                if curr_unit == next_unit:
                    count += 1

                else:
                    encoded_unit = struct.pack('B', count) + curr_unit
                    encoded += encoded_unit
                    encoded_content_size += len(
                        encoded_unit)  # Update the size of the encoded content
                    count = 1
            # encode the last unit
            encoded_unit = struct.pack('B', count) + curr_unit
            encoded += encoded_unit
            encoded_content_size += len(
                encoded_unit)  # Update the size of the encoded content
            # encoding the remaining bytes (outside the unit length)
            if bytes_num % self.unit_length != 0:
                encoded_unit = struct.pack('B', count) + content[
                                                         bytes_num - (
                                                                     bytes_num % self.unit_length):]
                encoded += encoded_unit
                encoded_content_size += len(
                    encoded_unit)  # Update the size of the encoded content

        return encoded, encoded_content_size
