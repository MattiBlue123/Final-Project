from compression_info import compression_info
from config import FLAGS, METADATA_FOOTER, METADATA_HEADER
from helper_functions import make_unique_path
from time import sleep


class ArchiveCreator:
    """The Archive class is responsible for creating a compressed archive of
    the files in the target directory. The archive is created in the target."""

    def __init__(self, metadata, encoded_content, pointer, target_dir,
                 archive_name, original_data_size, add_flag=False):
        self.metadata = metadata
        self.encoded_content = encoded_content
        self.pointer = pointer
        self.target_dir = target_dir
        self.archive_name = archive_name
        self.add_flag = add_flag
        self.original_data_size = original_data_size

    def process_metadata(self):
        """
        Process the metadata to be added to the archive as binary data.
        Returns:
        bytes: The processed metadata.
        """
        # Convert metadata to string and encode to bytes
        self.metadata = str(self.metadata)
        self.metadata = self.metadata.encode('utf-8')

        if not self.add_flag:
            # Add header and footer to the metadata
            header = METADATA_HEADER
            footer = METADATA_FOOTER
            return header + self.metadata + footer
        # this is meant so that while adding to an existing archive,
        # the metadata will not have the header and footer.
        return self.metadata

    def create_archive(self):
        """
        Create an archive of the compressed files in the target directory.
        :return:
        """
        # Create an archive of the compressed files
        self.metadata = self.process_metadata()
        if self.add_flag:
            return self.encoded_content, self.metadata
        self.encoded_content = self.encoded_content + self.metadata
        # naming the archive file
        # making sure there isn't an existing file with the same name.
        # adding a number to the name if there is.
        archive_path = make_unique_path(self.target_dir, self.archive_name +
                                        "_compressed")
        compression_info.archive_path = archive_path
        compression_info.original_data_size = self.original_data_size



        # saving the archive to the target directory
        with open(archive_path, 'wb') as archive:
            archive.write(self.encoded_content)
        if not self.add_flag:
            print(f"Archive created and saved to: {archive_path}\n\n")
            FLAGS["back flag"] = True
