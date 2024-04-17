import os
import compression_helper as ch
import compression as c

if __name__ == "__main__":
    valid_path = ch.PathValidator
    valid_target_dir = ch.TargetDirectoryValidator
    valid_unit_length = ch.UnitLengthValidator

    # the user inputs path or dir, it's validated and stored in paths, and is
    # being asked to enter more or type "ok" to continue
    all_paths = []
    while True:
        path = input("Enter a valid path or directory: ")
        if path.startswith('"') and path.endswith('"'):
            path = path.strip('""')
        path = valid_path(path).validate_path()
        all_paths.append(path)
        more = input(
            "Enter more paths or directories or type 'ok' to continue: ")
        if more.lower() == 'ok':
            break
    # the user inputs target directory, it's validated and stored in target_dir
    target_dir = input("Enter a valid target directory: ")
    target_dir = valid_target_dir(target_dir).validate_target_directory_input()

    # the user inputs unit length, it's validated and stored in unit_length
    unit_length = int(input("Enter a unit length: "))
    unit_length = valid_unit_length(unit_length).validate_unit_length_input()

    for path in all_paths:
        if os.path.isfile(path):
            compressor = c.FileCompressor(path, target_dir, unit_length)
            compressor.compress_and_save()
        elif os.path.isdir(path):
            compressor = c.FolderCompressor(path, target_dir, unit_length)
            compressor.compress_and_save()






