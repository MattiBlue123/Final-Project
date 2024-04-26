from encoder_update import RunLengthEncoder
import os


class Compressor:

    def compress_file(self, path, unit_length, path_in_archive):
        """
        Create metadata for a file.

        Parameters:
        path (str): The path of the file.
        unit_length (int): The unit length.
        path_in_archive (str): The path in the archive.

        Returns:
        dict: The metadata of the file.
        """
        encoded_file = b''
        encoder_update = RunLengthEncoder(path, unit_length,
                                          path_in_archive)

        encoded, header_length, encoded_size, hashed_content, original_size = (
            encoder_update.encode())
        file_metadata = dict()
        file_metadata["origin path"] = path
        file_metadata["path in archive"] = path_in_archive + ("/" +
                                                              os.path.basename(
                                                                  path))
        file_metadata["unit length"] = unit_length
        file_metadata["original size"] = original_size
        file_metadata["header length"] = header_length
        file_metadata["encoded size"] = encoded_size
        file_metadata["pointer"] = header_length + encoded_size
        file_metadata["data hash"] = hashed_content

        return file_metadata, encoded_file, file_metadata["pointer"]

    def compress_dir(self, path, unit_length, path_in_archive):
        """
        Create metadata for a directory.

        Parameters:
        path (str): The path of the directory.
        unit_length (int): The unit length.
        path_in_archive (str): The path in the archive.

        Returns:
        dict: The metadata of the directory.
        """
        encoded_dir = b''
        pointer = 0
        directory_metadata = dict()
        path_in_archive += "/" + os.path.basename(path)

        for file in os.listdir(path):
            file_path = os.path.join(path, file)

            if os.path.isdir(file_path):
                directory_metadata[file], encoded_dir = (path.compress_dir(
                    file_path, path_in_archive))

            else:
                if path_in_archive in directory_metadata.values():
                    raise ValueError(f"A file with the same name already "
                                     f"exists: {path_in_archive}")
                (directory_metadata[file], encoded_file,
                 file_pointer) = self.compress_file(
                    file_path, path_in_archive, unit_length)
                encoded_dir += encoded_file
                pointer += file_pointer

        return directory_metadata, encoded_dir

    def compress(self, path, unit_length):
        """
        Create metadata for a file or directory.

        Parameters:
        path (str): The path of the file or directory.
        unit_length (int): The unit length.
        path_in_archive (str): The path in the archive.

        Returns:
        dict: The metadata of the file or directory.
        """
        if os.path.isdir(path):
            return self.compress_dir(path, unit_length, path_in_archive="")
        else:
            return self.compress_file(path, unit_length, path_in_archive="")
        #
        # def __init__(self, metadata, target_dir):
        #     self.metadata = metadata
        #     self.target_dir = target_dir
        #
        # def __process_metadata(self, metadata, pointer, key=None):
        #     for key, value in metadata.items():
        #         if isinstance(value, dict):
        #             self.__process_metadata(value, key)
        #         else:
        #             encoder = RunLengthEncoder(value, pointer)
        #             file.encode()
        #
        #
        #
        # my_dict = {'key1': {'sub_key1': 1, 'sub_key2': 2},
        #            'key2': {'sub_key1': 3}}
        # iterate_nested_dict(my_dict)
        #
        # def compress(self):
        #     # This function will iterate over all the files in the all paths
        #     # list gets the path and saves it to "path", gets the unit length
        #     # and saves it to "unit_length" returns all_paths,
        #     # unit_lengths_for_paths
        #
        #     encoded = b''
        #     pointer = 0
        #     metadata, encoded = self.__process_metadata(metadata, pointer)
        #

        # iterates over paths.
        # for every type (file or directory) it will append a key to the
        # metadata with the file/folder name as the key and the value will
        # be an empty dictionary {}.
        # checks if that path is a file or a directory.

        # if  file - will compress it using the RunLengthEncoder and the
        # given unit length in the tuple from the all paths list.
        # the RLE returns the encoded content, the size of the encoded
        # content, the length of the header, and the sha-1 hash of the
        # file's original content.
        # the encoded content is appended to the encoded list.
        # the sizes of the encoded content and the unit length are saved
        # to the metadata dictionary.
        # pointer = pointer + length of the header + size of the encoded
        # content.
        # archive_path += "/" + the name of the file.

        # if directory - will call the method ones again with the following
        # values: all paths = the list of all the files in that directory,
        # unit_length = the unit length from the tuple in the all paths list,
        # archive_path = the path of the archive file (so far), metadata = the
        # metadata dictionary, pointer = the pointer, unit_length = the unit
        # length needed for all the following files in that directory.

        # if it's a directory, will call the method ones again to compress all
        # the files in that directory.
        #

        pass
