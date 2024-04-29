from config import FLAGS
import json
from helper_functions import make_unique_path
from add_to_archive import AddToArchive as AtA
class ArchiveCreator:
    """The Archive class is responsible for creating a compressed archive of
    the files in the target directory. The archive is created in the target."""

    def __init__(self, metadata, encoded_content, pointer, target_dir,
                 archive_name):
        self.metadata = metadata
        self.encoded_content = encoded_content
        self.pointer = pointer
        self.target_dir = target_dir
        self.archive_name = archive_name


    def process_metadata(self):
        """
        Process the metadata for JSON serialization.

        Returns:
        bytes: The processed metadata.
        """
        # Convert metadata to JSON and encode to bytes
        self.metadata = json.dumps(self.metadata)
        self.metadata = self.metadata.encode('utf-8')

        # Add header and footer to the metadata
        header = b'ZM\x01\x02'
        footer = b'ZM\x05\x06'
        return header + self.metadata + footer

    def create_archive(self, add_flag=False):
        # Create an archive of the compressed files

        self.encoded_content = self.encoded_content + self.process_metadata()
        # naming the archive file
        # making sure there isn't an existing file with the same name.
        # adding a number to the name if there is.
        archive_path = make_unique_path(self.target_dir, self.archive_name)

        with open(archive_path, 'wb') as archive:
            archive.write(self.encoded_content)
        if not add_flag:
            print(f"Archive created and saved to: {archive_path}")
            FLAGS["back flag"] = True
        else:
            return (archive_path, self.encoded_content,
                    self.metadata)

