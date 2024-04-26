import os.path
from helper_functions import zinput, create_metadata
from validator import (PathValidator as Pv, TargetDirectoryValidator as TdV,
                       UnitLengthValidator as UlV)
from compression import Compressor
from decompressor_init import DecompressorInit
from config import FLAGS

# say hello to user, explain rules
print("Welcome to the ZoZ RLE Compressor software.")
print("You can compress or decompress files using this software.")
print("At any time, you can type 'exit' to quit")

while True:
    user_input = zinput(
        "Do you want to compress (c) or decompress (d) files? ").lower().strip()
    if FLAGS["back_flag"]:
        print("Going back to main menu...")
        # Reset all changes here...
        FLAGS["back_flag"] = False
        continue
    if user_input == ('compress' or 'compress files' or 'c'):
        # initialize validators
        encoded = b''
        metadata = dict()
        path = Pv(zinput(
            "please input one path at a time: ").strip('""')).validate_path()
        archive_name = os.path.basename(path)
        unit_length = UlV(zinput(
            'the program is set to a default unit length '
            'of 1. if you want to change it, enter a new numeric value.'
            ' Otherwise, press "Enter": ').strip('""')).validate_unit_length()

        metadata[archive_name] = create_metadata(path, unit_length,
                                                 archive_name)
        while True:
            path = zinput(
                "Enter another path or type 'ok' to continue: ").strip('""')
            if path.lower() == 'ok':
                break
            else:
                # validate the paths
                path = Pv(path).validate_path()
                unit_length = zinput("Enter unit length: ").strip('""')
                unit_length = UlV(unit_length).validate_unit_length()
                path_name = os.path.basename(path)
                metadata[os.path.basename(path)] = create_metadata(path,
                                                                   unit_length,
                                                                   path_name)

        # get user input of target directory
        target_dir = zinput("Please enter the target directory: ").strip('""')
        target_dir = TdV(target_dir).validate_target_directory()

        compressor = Compressor(metadata, target_dir, archive_name)
        compressor.compress()

    elif user_input == 'decompress' or 'decompress files' or 'd':
        d = DecompressorInit()
        d.decompressor_init_main()

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
