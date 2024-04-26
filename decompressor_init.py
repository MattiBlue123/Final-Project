import json
import os
from config import DI_PROMPTS, DI_POSSIBLE_ACTIONS
from helper_functions import zinput
from validator import PathValidator as Pv, TargetDirectoryValidator as TdV


class DecompressorInit:

    def __init__(self):
        # self.path = self._get_path()
        self.path = r"C:\Users\zohar\OneDrive\Desktop\Test Cases\Text\test.txt_rle_compressed.bin"
        self.metadata = None
        self.target_dir = None

    @staticmethod
    def _get_path():
        path = Pv(zinput(
            "Please enter the path to the archive file: ").strip(
            '""')).validate_path()
        return path

    def get_target_dir(self):
        target_dir = zinput("Please enter the target directory: ").strip('""')
        target_dir = TdV(target_dir).validate_target_directory()
        return target_dir

    def get_metadata(self):
        with open(self.path, 'rb') as f:
            f.seek(-4, os.SEEK_END)
            footer = f.read()

            if footer != b'ZM\x05\x06':
                raise ValueError("Invalid archive")

            is_header = bytearray()
            metadata_length = 0

            while f.tell() > 0:  # While not at the start of the file
                f.seek(-1, os.SEEK_CUR)  # Move the pointer back 1 byte
                byte = f.read(1)  # Read the byte
                is_header.insert(0, byte[
                    0])  # Add the byte to the start of the found sequence
                metadata_length += 1  # Increment the header_length
                if len(is_header) > 4:  # If the found sequence
                    # is too long
                    is_header.pop()  # Remove the last byte from the found sequence
                if is_header == b'ZM\x01\x02':  # If the found sequence
                    # matches the target sequence
                    f.seek(3, os.SEEK_CUR)
                    metadata = f.read(
                        metadata_length - 8)  # avoid reading the footer
                    metadata = metadata.decode('utf-8')
                    self.metadata = json.loads(metadata)
                    break
                f.seek(-1, os.SEEK_CUR)

            if 'metadata' not in locals():
                raise ValueError("Invalid archive")

    def get_content_directory(self, dictionary, path='', start=''):
        for key, value in dictionary.items():
            new_path = f'{path}/{key}' if path else key
            if isinstance(value, dict):
                # If the dictionary has any nested dictionaries, don't print the current path
                if any(isinstance(v, dict) for v in value.values()):
                    self.get_content_directory(value, new_path, start)
                elif new_path.startswith(start):
                    print(new_path)
            else:
                continue

    def user_path_input_validation(self):
        while True:
            self.path = zinput("please input one path at a time: ").strip('""')
            if not Pv(self.path).validate_path():
                print("Invalid path")
                continue
            break
        return self.path

    def get_response(self):
        while True:
            response = zinput(DI_PROMPTS["get input"]).lower().split()
            if len(response) == 0 or len(response) > 3:
                print("Invalid response")
                continue
            if response[0] not in DI_POSSIBLE_ACTIONS:
                print("Invalid response")
                continue
            if len(response) == 1:
                return response

            if response == 'd help':
                print(DI_POSSIBLE_ACTIONS["d help"])
                continue
            if response == '
                continue
        return response



    def decompressor_init_main(self):
        print(DI_PROMPTS["d help"])
        user_input = self.get_response()


        # self._get_path()
        self.get_metadata()
        # self.target_dir = self.get_target_dir()
        self.target_dir = r'C:\Users\zohar\OneDrive\Desktop\Test Cases\Text'

        zinput(actions_str)


if __name__ == '__main__':
    d = DecompressorInit()
    d.decompressor_init_main()
