import os
import struct
import json

class RunLengthDecoder:
    def __init__(self, file_path, save_path):
        self.file_path = file_path
        self.save_path = save_path

    def decode(self):
        # Open the encoded file in binary mode
        with open(self.file_path, 'rb') as f:
            content = f.read()

        # Separate the header from the encoded content
        header, encoded_content = content.split(b'\n', 1)

        # Parse the header to retrieve the original file's metadata
        header_data = json.loads(header.decode('utf-8'))

        # Decode the encoded content
        decoded_content = b''
        i = 0
        while i < len(encoded_content):
            count = struct.unpack('B', encoded_content[i:i + 1])[0]
            unit = encoded_content[i + 1:i + 1 + header_data['unit_length']]
            decoded_content += unit * count
            i += 1 + header_data['unit_length']

        # Write the decoded content to a new file
        with open(os.path.join(self.save_path, header_data['file_name']), 'wb') as f:
            f.write(decoded_content)