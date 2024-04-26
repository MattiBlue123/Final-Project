import json
import os
from config import DI_PROMPTS, DI_POSSIBLE_ACTIONS
from helper_functions import zinput, validate_path_format, parse_archive_path
from validator import PathValidator as Pv, TargetDirectoryValidator as TdV
from decompression import Decompressor


class DecompressorInit:

    def __init__(self):
        self.path_to_archive = ""
        self.metadata_length = 0
        self.metadata = {}
        self.target_dir = ''


    def get_path(self):
        while True:
            path = Pv(zinput(
                "Please enter the path to the archive file: ").strip(
                '""')).validate_path()
            if not os.path.isfile(path):
                print("Invalid path")
                continue
            self.path_to_archive = path
            break

    def get_target_dir(self):
        target_dir = zinput("Please enter the target directory: ").strip('""')
        self.target_dir = TdV(target_dir).validate_target_directory()

    def get_metadata(self):
        with open(self.path_to_archive, 'rb') as f:
            print(f"Reading metadata from {self.path_to_archive}")
            f.seek(-4, os.SEEK_END)
            footer = f.read()

            if footer != b'ZM\x05\x06':
                raise ValueError("Invalid archive")

            is_header = bytearray()

            while f.tell() > 0:  # While not at the start of the file
                f.seek(-1, os.SEEK_CUR)  # Move the pointer back 1 byte
                byte = f.read(1)  # Read the byte
                is_header.insert(0, byte[
                    0])  # Add the byte to the start of the found sequence
                self.metadata_length += 1  # Increment the header_length
                if len(is_header) > 4:  # If the found sequence
                    # is too long
                    is_header.pop()  # Remove the last byte
                if is_header == b'ZM\x01\x02':  # If the found sequence
                    # matches the target sequence
                    f.seek(3, os.SEEK_CUR)
                    self.metadata_length -= 4
                    metadata = f.read(
                        self.metadata_length - 4)  # avoid reading the footer
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
                # if it has files or folders, only print their paths
                if any(isinstance(v, dict) for v in value.values()):
                    self.get_content_directory(value, new_path, start)
                elif new_path.startswith(start):
                    print(new_path)
            elif new_path.startswith(start):  # print files as well
                print(new_path)

    def archive_path_validation(self):
        while True:
            self.path_to_archive = zinput(
                "please input the path of the archive file: ").strip('""')
            if not Pv(self.path_to_archive).validate_path():
                print("Invalid path")
                continue
            break
        return self.path_to_archive

    def validate_path_in_archive(self, archive_path_input):
        if not validate_path_format(archive_path_input):
            raise ValueError("Invalid path format")
        # Parse the archive path into a list of keys
        parsed_path = parse_archive_path(archive_path_input)

        # Start with the root of the dictionary
        current_dict = self.metadata

        # For each key in the parsed path
        for key in parsed_path:
            # make sure key exist and is a file\folder
            if key in current_dict and isinstance(current_dict[key], dict):
                # if it's a folder, move to the next level of the dictionary
                current_dict = current_dict[key]
            else:
                # if file/folder not found in directory, raise exception
                raise ValueError("Invalid path in archive")

        # If you have checked all keys without returning False, return True
        return True

    def get_response(self):
        while True:
            response = zinput(DI_PROMPTS["get input"]).lower().split()
            if len(response) == 0 or len(response) > 2:
                print("Invalid response")
                continue
            if response[0] not in DI_POSSIBLE_ACTIONS:
                print("Invalid response")
                continue
            if response[0] == 'dhelp':
                print(DI_PROMPTS["dhelp"])
                continue
            if response[0] == 'show' or response[0] == 'extract':
                # validate path in archive
                if len(response) == 1:  # path hasn't been provided
                    return response
                if not self.validate_path_in_archive(response[1]):
                    print("Invalid path in archive")
                    continue
            return response

    def get_relevant_metadata(self, path):
        path = parse_archive_path(path)
        current_dict = self.metadata
        for key in path:
            current_dict = current_dict[key]
        return current_dict

    def input_decesion_tree(self, user_input):
        if user_input[0] == 'show' and len(user_input) == 1:
            return self.get_content_directory(self.metadata)

        elif user_input[0] == 'show' and len(user_input) == 2:
            return self.get_content_directory(self.metadata,
                                              start=user_input[1])
        elif user_input[0] == 'extract':
            try:
                if len(user_input) == 2:  # extract specific files
                    # get relevant metadata only for the files to extract
                    self.metadata = self.get_relevant_metadata(user_input[1])
                decompressor = Decompressor(self.path_to_archive,
                                            self.target_dir, self.metadata,
                                            self.metadata_length)
                decompressor.extract()
            except Exception as e:
                print(f"Error extracting files: {e}")

    def decompressor_init_main(self):
        print(DI_PROMPTS["dhelp"])
        self.get_path()
        print(f"{self.path_to_archive}")
        self.get_metadata()
        self.get_target_dir()
        while True:
            user_input = self.get_response()
            self.input_decesion_tree(user_input)


