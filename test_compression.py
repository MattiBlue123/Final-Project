import unittest
from unittest.mock import patch
from WorkOnArchive import WorkOnArchive
from compression_init import CompressorInit
from time import sleep


# class TestCompressorInit(unittest.TestCase):
#     @patch('compression_init.zinput', create=True)
#     def test_compressor_init_main(self, mock_zinput):
#         # Arrange
#         mock_zinput.side_effect = [
#             '1',  # unit length
#             r"C:\Users\zohar\OneDrive\Desktop\Test Cases\Text\Text2",  # path
#             r"C:\Users\zohar\OneDrive\Desktop\open",  # target directory
#             "ok" # no more paths
#         ]
#         compressor_init = CompressorInit()
#
#         # Act
#         compressed_output = compressor_init.compressor_init_main()


class TestDecompressorInit(unittest.TestCase):
    @patch('decompression_init.zinput', create=True)
    def test_decompressor_init_main(self, mock_zinput):
        # Arrange
        mock_zinput.side_effect = [
            r"C:\Users\zohar\OneDrive\Desktop\open\Text2_compressed(3)_compressed",
            'extract',
            "C:\\Users\\zohar\\OneDrive\\Desktop\\open"]
        decompressor_init = WorkOnArchive()

        # Act
        decompressor_init.work_on_archive_main()



if __name__ == '__main__':
    unittest.main()
