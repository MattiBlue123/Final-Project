import os.path
from helper_functions import zinput, create_metadata
from validator import (PathValidator, TargetDirectoryValidator,
                       UnitLengthValidator)
from compression import Compressor

# say hello to user, explain rules
print("Welcome to the ZoZ RLE Compressor software.")
print("You can compress or decompress files using this software.")
print("At any time, you can type 'exit' to quit")

while True:
    user_input = zinput(
        "Do you want to compress (c) or decompress (d) files? ").lower().strip()
    if user_input == 'compress' or 'compress files' or 'c':
        # initialize validators
        encoded = b''
        valid_path = PathValidator
        valid_target_dir = TargetDirectoryValidator
        valid_unit_length = UnitLengthValidator
        metadata = dict()
        path = zinput("please input one path at a time: ").strip('""')
        path = valid_path(path).validate_path()
        # path = validate_path(path)
        archive_name = os.path.basename(path)
        unit_length = valid_unit_length(zinput(
            'the program is set to a default unit length '
            'of 1. if you want to change it,'
            ' enter a new numeric value.'
            ' Otherwise, press "Enter": ').strip(
            '""')).validate_unit_length()
        metadata[archive_name] = create_metadata(path, unit_length,
                                                 archive_name)
        while True:
            path = zinput(
                "Enter another path or type 'ok' to continue: ").strip('""')
            if path.lower() == 'ok':
                break
            else:
                # validate the paths
                path = valid_path(path).validate_path()
                unit_length = valid_unit_length(zinput("Enter unit length: ")
                                                ).validate_unit_length()
                archive_name = os.path.basename(path)
                metadata[os.path.basename(path)] = create_metadata(path,
                                                                   unit_length,
                                                                   archive_name)
        # path = r"C:\Users\zohar\OneDrive\Desktop\Test Cases\Text"
        # unit_length = 1


        # get user input of target directory
        target_dir = valid_target_dir(zinput(
            "Enter target directory: ").strip(
            '""')).validate_target_directory()
        # target_dir = r"C:\Users\zohar\OneDrive\Desktop\Test Cases\Test"
        # iterate_nested_dict(metadata)
        compressor = Compressor(metadata, target_dir, archive_name)
        compressor.compress()






    # elif user_input == 'decompress':
        # show user the root
#     # get user input of the path of the archive file
#     # validate the path
#     # validate is archive file
#     # assume target dir for decoded file is the same as the target dir of
#     # the archive file, user can input a different target dir
#     # if different target dir = true:
#     # validate the target dir
#
#     # call decompression function to decompress the files
#     # store save files to the target dir
#     else:
#         print("Invalid input. Please try again")
#         continue
#
#
#
# """
