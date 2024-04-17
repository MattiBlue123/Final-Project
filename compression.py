import os
import compression_helper as ch


class FileCompressor:
    def __init__(self, file_path, target_directory, unit_length):
        self.file_path = file_path
        self.target_location = target_directory
        self.unit_length = unit_length

    def compress_and_save(self):

        # Create a RunLengthEncoder instance
        rle_encoder = ch.RunLengthEncoder(self.file_path, self.unit_length)

        # Compress the content
        compressed_content = rle_encoder.encode()

        # Save the compressed content to the target location
        original_file_name = \
            os.path.splitext(os.path.basename(self.file_path))[0]
        counter = None
        while True:
            suffix = f"_{counter}" if counter is not None else ""
            target_file_name = f"{original_file_name}_rle_compressed{suffix}.bin"
            target_file_path = os.path.join(self.target_location,
                                            target_file_name)
            if not os.path.exists(target_file_path):
                break
            counter = 1 if counter is None else counter + 1

        with open(target_file_path, 'wb') as target_file:
            target_file.write(compressed_content)

        print(f"File compressed and saved to: {target_file_path}")


class BatchCompressor:
    pass


class FolderCompressor:
    pass


class CompressionInfo:
    pass
