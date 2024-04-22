from compression import ArchiveCreator, BatchCompressor
from everything_validator import (PathValidator, TargetDirectoryValidator,
                                  UnitLengthValidator)
from decompression import RunLengthDecoder

if __name__ == "__main__":
    valid_path = PathValidator
    valid_target_dir = TargetDirectoryValidator
    valid_unit_length = UnitLengthValidator

    # the user inputs path or dir, it's validated and stored in paths, and is
    # being asked to enter more or type "ok" to continue
    all_paths = []
    path = input("Enter path or directory to be compressed: ").strip('""')
    path = valid_path(path).validate_path()
    all_paths.append(path)
    while True:
        more = input(
            "Enter more paths or directories or type 'ok' to continue: ").strip('""')
        if more.lower() == 'ok':
            break
        else:
            path = valid_path(more).validate_path()
            all_paths.append(path)

    # the user inputs target directory, it's validated and stored in target_dir
    target_dir = input("Enter a target directory: ").strip('""')
    target_dir = valid_target_dir(target_dir).validate_target_directory_input()

    # the user inputs unit length, it's validated and stored in unit_length
    unit_length = int(input("Enter a unit length: "))
    unit_length = valid_unit_length(unit_length).validate_unit_length_input()

    # Create a BatchCompressor instance
    batch_compressor = BatchCompressor(all_paths, target_dir, unit_length)
    # Compress the files
    compressed_files_lst = batch_compressor.compress_files()
    archive = ArchiveCreator(compressed_files_lst, target_dir)
    archive.create_archive()

    # Ask the user which file to decode
    file_to_decode = input("Enter the path of the file to decode: ").strip('""')
    file_to_decode = valid_path(file_to_decode).validate_path()

    # Ask the user where to save the decoded file
    save_path = input("Enter the path where the decoded file should be saved: ").strip('""')
    save_path = valid_target_dir(save_path).validate_target_directory_input()

    # Recreate the original file from the compressed file
    decompress = RunLengthDecoder(file_to_decode, save_path)
    decompress.decode()

