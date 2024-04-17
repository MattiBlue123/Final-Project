import unittest
import os
from compression import FileCompressor
from compression_helper import RunLengthEncoder, FileTypeChecker, \
    InputValidator


class TestRunLengthEncoder(unittest.TestCase):
    def setUp(self):
        self.file_path = 'path_to_test_file'  # replace with path to a test file
        self.file_type = FileTypeChecker(self.file_path).get_file_type()
        self.unit_length = 1
        self.encoder = RunLengthEncoder(self.file_path, self.file_type,
                                        self.unit_length)

    def test_encode_text_file(self):
        # Test encoding of a text file
        if self.file_type == "text":
            encoded_content = self.encoder.encode(self.file_path,
                                                  self.file_type)
            self.assertIsInstance(encoded_content, bytes)

    def test_encode_binary_file(self):
        # Test encoding of a binary file
        if self.file_type == "binary":
            encoded_content = self.encoder.encode(self.file_path,
                                                  self.file_type)
            self.assertIsInstance(encoded_content, bytes)

    def test_encode_invalid_file_type(self):
        # Test encoding of an invalid file type
        encoded_content = self.encoder.encode(self.file_path, "invalid")
        self.assertEqual(encoded_content, "Invalid file type")


class TestInputValidator(unittest.TestCase):
    def setUp(self):
        self.file_path = 'path_to_test_file'  # replace with path to a test file
        self.target_directory = 'path_to_target_directory'  # replace with path to a target directory
        self.unit_length = 1
        self.validator = InputValidator(self.file_path, self.target_directory,
                                        self.unit_length)

    def test_valid_inputs(self):
        # Test valid inputs
        self.assertTrue(self.validator.are_inputs_valid())

    def test_invalid_file_path(self):
        # Test invalid file path
        self.validator.path = 'invalid_path'
        self.assertFalse(self.validator.is_valid_file_path())

    def test_invalid_target_directory(self):
        # Test invalid target directory
        self.validator.target_directory = 'invalid_directory'
        self.assertFalse(self.validator.is_valid_target_directory())

    def test_invalid_unit_length(self):
        # Test invalid unit length
        self.validator.unit_length = 0
        self.assertFalse(self.validator.is_valid_unit_length())


class TestFileCompressor(unittest.TestCase):
    def setUp(self):
        self.file_path = 'path_to_test_file'  # replace with path to a test file
        self.target_location = 'path_to_target_location'  # replace with path to a target location
        self.unit_length = 1
        self.compressor = FileCompressor(self.file_path, self.target_location,
                                         self.unit_length)

    def test_compress_and_save(self):
        self.compressor.compress_and_save()
        expected_file_path = os.path.join(self.target_location,
                                          os.path.splitext(os.path.basename(
                                              self.file_path))[
                                              0] + "_rle_compressed.bin")
        self.assertTrue(os.path.exists(expected_file_path),
                        "Compressed file does not exist")

    def test_compress_and_save_invalid_path(self):
        invalid_path = 'invalid_path'
        self.compressor.file_path = invalid_path
        with self.assertRaises(FileNotFoundError):
            self.compressor.compress_and_save()


if __name__ == '__main__':
    unittest.main()
