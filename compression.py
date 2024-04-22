import os
from encoder import RunLengthEncoder
import uuid


class BatchCompressor:

    def __init__(self, all_paths, target_dir, unit_length):
        self.all_paths = all_paths
        self.target_dir = target_dir
        self.unit_length = unit_length
        self.metadata = {}

    def compress_files(self):
        compressed_files_lst = []
        # # saves the name of the first file or folder, so it'll be the name
        # # of the archive
        # compressed_files_lst = [os.path.basename(self.all_paths[0])]

        for path in self.all_paths:
            if os.path.isdir(path):
                folder_name = os.path.basename(path)

                # saves the number of files in the folder being compressed
                files_num = str(len([item for item in os.listdir(
                    path) if os.path.isfile(os.path.join(path, item))]))

                for item in os.listdir(path):
                    file_path = os.path.join(path, item)

                    # Create a RunLengthEncoder instance
                    file_to_compress = RunLengthEncoder(file_path,
                                                        self.unit_length,
                                                        folder_name, files_num)
                    compressed_files_lst.append(file_to_compress.encode())
            else:
                encoder = RunLengthEncoder(path, self.unit_length)
                file_id = uuid.uuid4().bytes
                encoded_content, size, file_id = encoder.encode()
                # Add the metadata of the file to the dictionary
                self.metadata[path] = {"id": file_id,
                                       "unit_length": self.unit_length,
                                       "size": size}
                # Add the encoded content to the compressed files list
                compressed_files_lst.append(encoded_content)
        return compressed_files_lst

class ArchiveCreator:
    """The Archive class is responsible for creating a compressed archive of
    the files in the target directory. The archive is created in the target."""

    def __init__(self, compressed_files_lst, target_dir):
        self.compressed_files_lst = compressed_files_lst
        self.target_dir = target_dir

    def create_archive(self):
        # Create an archive of the compressed files

        # naming the archive
        original_file_name = os.path.basename(self.compressed_files_lst[0])
        self.compressed_files_lst.pop(0)
        # making sure there isn't an existing file with the same name.
        # adding a number to the name if there is.
        counter = None
        while True:
            suffix = f"_{counter}" if counter is not None else ""
            archive_name = f"{original_file_name}_rle_compressed{suffix}.bin"
            archive_path = os.path.join(self.target_dir, archive_name)

            if not os.path.exists(archive_path):
                break
            counter = 1 if counter is None else counter + 1

        with open(archive_path, 'wb') as archive:
            for compressed_file in self.compressed_files_lst:
                archive.write(compressed_file)
        print(f"Archive created and saved to: {archive_path}")
