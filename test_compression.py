import unittest
from unittest.mock import patch
from work_on_archive import WorkOnArchive
from compression_init import CompressorInit

#
# class TestCompressorInit(unittest.TestCase):
#     @patch('compression_init.zinput', create=True)
#     def test_compressor_init_main(self, mock_zinput):
#         # Arrange
#         mock_zinput.side_effect = [
#             '1',  # unit length
#             r"C:\Users\zohar\OneDrive\Desktop\test files\empty.txt",  # path
#             r"C:\Users\zohar\OneDrive\Desktop\open",  # target directory
#             "ok"  # no more paths
#         ]
#         compressor_init = CompressorInit()
#
#         # Act
#         compressed_output = compressor_init.compressor_init_main()



class TestWorkOnArchive(unittest.TestCase):
    @patch('work_on_archive.zinput', create=True)
    def test_work_on_archive(self, mock_zinput):
        # Arrange
        mock_zinput.side_effect = [
            r"C:\Users\zohar\OneDrive\Desktop\open\empty.txt_compressed",
            'extract',
            "C:\\Users\\zohar\\OneDrive\\Desktop\\open"]
        work_on_archive = WorkOnArchive()

        # Act
        work_on_archive.work_on_archive_main()


if __name__ == '__main__':
    unittest.main()
