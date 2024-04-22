import unittest
from unittest.mock import patch
from main import ArchiveCreator, BatchCompressor, PathValidator, TargetDirectoryValidator, UnitLengthValidator
import os

class TestMain(unittest.TestCase):
    def setUp(self):
        self.test_dir = "C:\\Users\\zohar\\OneDrive\\Desktop\\Test Cases"
        self.test_cases = [os.path.join(self.test_dir, dir) for dir in os.listdir(self.test_dir) if os.path.isdir(os.path.join(self.test_dir, dir))]

    @patch('builtins.input',
           side_effect=['test_path', 'ok', 'test_target_dir', '1',
                        'test_target_dir'])
    def test_main(self, input):
        # rest of your code
        valid_path = PathValidator
        valid_target_dir = TargetDirectoryValidator
        valid_unit_length = UnitLengthValidator

        for test_case in self.test_cases:
            all_paths = []
            path = valid_path(test_case).validate_path()
            all_paths.append(path)

            target_dir = valid_target_dir('test_target_dir').validate_target_directory_input()

            unit_length = int('1')
            unit_length = valid_unit_length(unit_length).validate_unit_length_input()

            batch_compressor = BatchCompressor(all_paths, target_dir, unit_length)
            compressed_files_lst = batch_compressor.compress_files()
            archive = ArchiveCreator(compressed_files_lst, target_dir)
            archive_file = archive.create_archive()

            self.assertTrue(os.path.exists(archive_file), f"Archive file not created for test case: {archive_file}")

            print(f"Compression successful for test case: {test_case}")

            os.remove(archive_file)

            self.assertFalse(os.path.exists(archive_file), f"Failed to delete archive file for test case: {archive_file}")

if __name__ == "__main__":
    unittest.main()