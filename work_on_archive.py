import ast
import os
import time
from typing import Dict
from config import *
from helper_functions import zinput, make_unique_path
from validator import (PathValidator as Pv, TargetDirectoryValidator as TdV,
                       ArchiveValidator as Av)
from decompression import Decompressor
from add_to_archive import AddToArchive as AtA


class WorkOnArchive:
    """
    This class is responsible for working on an existing archive.
     It allows the user to extract files, add files,
      and show the content of the archive.
    """

    def __init__(self):
        self.path_to_archive = ""
        self.metadata_length = 0
        self.metadata = {}
        self.target_dir = ''
        self.av = None

    def get_path(self) -> None:
        """
        This function gets the path to the archive
         file from the user and validates it.
        :return:
        """
        while True:
            path = Pv(zinput(
                "Please enter the path to the archive file: ").strip(
                '""')).validate_path()
            if not os.path.isfile(path):
                print("Invalid path")
                continue
            self.path_to_archive = path
            break

    def get_target_dir(self) -> None:
        """
        This function gets the target directory from the user and validates it.
        :return:
        """
        target_dir = zinput("Please enter the target directory: ").strip('""')
        self.target_dir = TdV(target_dir).validate_target_directory()

    def get_metadata(self) -> bool:
        """
        Reads the metadata from the archive file and validates it.
        :return:
        """
        try:
            with open(self.path_to_archive, 'rb') as f:
                print(f"Reading metadata from {self.path_to_archive}")
                f.seek(-METADATA_FOOTER_LENGTH, os.SEEK_END)
                footer = f.read()

                if footer != METADATA_FOOTER:
                    raise ValueError(
                        f"Invalid archive: Missing footer in"
                        f" {self.path_to_archive}")

                is_header = bytearray()

                while f.tell() > 0:  # While not at the start of the file
                    f.seek(-1, os.SEEK_CUR)  # Move the pointer back 1 byte
                    byte = f.read(1)  # Read the byte
                    # Add the byte to the start of the found sequence
                    is_header.insert(0, byte[0])
                    self.metadata_length += 1  # Increment the header_length
                    if len(is_header) > METADATA_HEADER_LENGTH:  # too long
                        is_header.pop()  # Remove the last byte
                        # If the found sequence matches the target sequence
                    if is_header == METADATA_HEADER:
                        f.seek(3, os.SEEK_CUR)
                        self.metadata_length -= METADATA_HEADER_LENGTH
                        # avoid reading the footer
                        metadata = f.read(
                            self.metadata_length - METADATA_HEADER_LENGTH)
                        metadata = metadata.decode('utf-8')
                        # convert the string to a dictionary

                        self.metadata = ast.literal_eval(metadata)

                        # the process didn't return a dictionary
                        if not self.metadata:
                            raise ValueError(f"Metadata is not a valid "
                                             f"dictionary: {metadata}")

                        break
                    f.seek(-1, os.SEEK_CUR)

                self.av = Av(self.path_to_archive, self.metadata)
                if not self.av.validate_metadata():
                    print("Invalid metadata: archive's metadata format is "
                          "invalid")
                    return False
        except ValueError as e:
            print(f"Error reading metadata: {e}")
            return False
        except SyntaxError:
            print(
                f"Error parsing metadata {self.path_to_archive}:"
                f" Invalid syntax")
            return False
        except IOError as e:
            print(f"Error opening file {self.path_to_archive}: {e}")
            return False
        except UnicodeDecodeError as e:
            print(f"Error decoding metadata in {self.path_to_archive}: {e}")
            return False

        return True

    def get_content_directory(self, dictionary: Dict, path: str = '',
                              start: str = '') -> None:
        """
        This function prints the content of the archive for the "show" command.
        :param:
        dictionary (dict): The dictionary to print.
        path (str): The path in the archive.
        start (str): The start of the path.
        :return:
        None
        """
        for key, value in dictionary.items():
            new_path = f'{path}/{key}' if path else key
            if isinstance(value, dict):
                # if it has files or folders, only print their paths
                if any(isinstance(v, dict) for v in value.values()):
                    self.get_content_directory(value, new_path, start)
                elif new_path.startswith(start):
                    print(new_path)
            elif new_path.startswith(start) and key == "type" and isinstance(
                    value, dict):
                print(new_path)

    def get_relevant_metadata(self, path: str) -> bool:
        """
        This function gets the relevant metadata for the files to extract.
        The user can input a path to a file or a directory, and we need to
        extract only them, for that we need to set the metadata to the relevant
        :param:
        path (str): The path in the archive.
        :return:
        bool: True if the path is valid, False otherwise
        """
        path = self.av.parse_path_in_archive(path)
        current_dict = self.metadata
        for key in path:
            if key in current_dict and isinstance(current_dict[key], dict):
                current_dict = current_dict[key]
            else:
                return False
        # Create a new dictionary with the filename as the key
        self.metadata = {path[-1]: current_dict}
        return True

    def get_response(self) -> list:
        """
        This function gets the user input and validates it.
        :return:
        list: The user input
        """
        while True:
            response = zinput(WOA_PROMPTS["get input"])
            if ' ' in response:
                command, path = response.split(' ', 1)
                response = [command, path]
            else:
                response = response.split()
            if len(response) == 0 or len(response) > 2:
                print("Invalid response")
                continue
            if response[0] not in WOA_POSSIBLE_ACTIONS:
                print("Invalid response")
                continue
            if response[0] == '--whelp':
                print(WOA_PROMPTS["--whelp"])
                continue
            if response[0] == 'show' or response[0] == 'extract':
                # validate path in archive
                if len(response) == 1:  # path hasn't been provided
                    return response
                if not self.av.validate_path_in_archive(response[1]):
                    print("Invalid path in archive or path format")
                    continue
            return response

    def input_decision_tree(self, user_input: list) -> bool:
        """
        This function is the decision tree for the user input.
        :param:
        user_input (list): The user input.
        :return:
        bool: True if the user wants to continue working on the archive,
         False otherwise.
        """

        if user_input[0] == 'show' and len(user_input) == 1:
            self.get_content_directory(self.metadata)
            return True

        elif user_input[0] == 'show' and len(user_input) == 2:
            self.get_content_directory(self.metadata,
                                       start=user_input[1].lstrip('/'))
            return True

        elif user_input[0] == 'extract':
            if len(user_input) == 2:  # extract specific files
                # get relevant metadata only for the files to extract
                if not self.get_relevant_metadata(user_input[1]):
                    print("Invalid path in archive")
                    return True

            self.get_target_dir()
            target_dir_name = os.path.basename(self.path_to_archive)
            if "_compressed" in target_dir_name:
                target_dir_name = target_dir_name.replace("_compressed",
                                                          "_extracted")
            self.target_dir = make_unique_path(self.target_dir,
                                               target_dir_name)
            os.mkdir(self.target_dir)
            decompressor = Decompressor(self.path_to_archive,
                                        self.target_dir, self.metadata)
            print("extracting...")
            decompressor.extract()

        if user_input[0] == 'add':
            # moving to add_to_archive.py
            add_to_archive = AtA(self.path_to_archive, self.metadata)
            add_to_archive.add_file_to_archive()

    def work_on_archive_main(self) -> None:
        """
        This function is the main function for working on an archive.
        """
        print(WOA_PROMPTS["--whelp"])
        while True:
            self.get_path()
            # get metadata from archive, it also validates the metadata,
            # returns True if successful
            if not self.get_metadata():
                time.sleep(1)
                continue
            break
        while True:
            user_input = self.get_response()
            if not self.input_decision_tree(user_input):
                break
