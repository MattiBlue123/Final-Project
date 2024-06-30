import time
from pathlib import Path
from typing import Dict, Any

from gui import CompressionInfoGUI
from config import FILE_HEADER_LENGTH


class CompressionInfo:
    def __init__(self):
        self.files_compression_info = []
        self.overall_size_diff = 0
        self.archive_path = None
        self.original_data_size = 0

    def add_info(self, file_name: str, runtime: float, compressed_by: str) \
            -> None:
        """
        :param:
        file_name (str): The name of the file.
        runtime (int): The time taken to compress the file.
        compressed_by (float): The size diff before and after compression.
        :return:
        None
        """
        self.files_compression_info.append((file_name, runtime, compressed_by))

    def compression_stats_gui(self) -> None:
        """
        The calling function for the CompressionInfoGUI
        :return:
        None
        """
        gui = CompressionInfoGUI(self)
        gui.mainloop()

    def reset(self) -> None:
        """
        Resets the compression info between runs
        :return:
        None
        """
        self.files_compression_info = []
        self.overall_size_diff = 0


compression_info = CompressionInfo()


def file_compressing_timer_decorator(func: callable) -> callable:
    """
    Decorator function to measure the time taken to compress a file
     and calculate the size difference before and after compression.

    :param:
    func (callable): The function to be decorated.
    :return:
    The decorated function.
    """

    def wrapper(self, metadata: Dict, pointer: int = 0) -> Any:
        """
        Wrapper function that is called instead of the decorated function.

        :param:
        self (Compressor): The instance of the class where the decorated
        function is defined.
        metadata (Dict): The metadata of the file to be compressed.
        pointer (int): The pointer to the file in the archive.
        :return:
        The result of the decorated function.
        """
        file_path = Path(metadata["origin path"])
        # not to be confused with two files with the same name
        # in different directories
        file_name = f"{file_path.parent.name}/{file_path.stem}"
        start_time = time.time()
        result = func(self, metadata, pointer)
        end_time = time.time()
        runtime = end_time - start_time

        compressed_by = metadata["original size"] - metadata["encoded size"]
        compressed_by -= FILE_HEADER_LENGTH
        # if the file was expanded, compressed_by will be negative
        if compressed_by < 0:
            compression_info.overall_size_diff -= compressed_by
            compressed_by = "expanded by " + str(abs(compressed_by))

        # if the file was compressed, compressed_by will be positive
        else:
            compression_info.overall_size_diff -= compressed_by
            compressed_by = "compressed by " + str(compressed_by)
        compression_info.add_info(file_name, runtime, compressed_by)
        return result

    return wrapper


def archiving_timer_decorator(func: callable) -> callable:
    """
    Decorator function to measure the time taken to create an
    archive and calculate the overall size difference.

    :param func: The function to be decorated.
    :return: The decorated function.
    """

    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that is called instead of the decorated function.

        :param self: The instance of the class where
         the decorated function is defined.
        :param args: The positional arguments passed to the decorated function.
        :param kwargs: The keyword arguments passed to the decorated function.
        :return: The result of the decorated function.
        """
        start_time = time.time()
        result = func(self, *args, **kwargs)
        end_time = time.time()
        runtime = end_time - start_time
        add_flag = kwargs.get('add_flag', False)
        if add_flag:
            compression_info.archive_path = kwargs.get('archive_path', '')

        # if the overall size difference is negative, the archive was expanded

        compression_info.overall_size_diff = calculate_overall_diff()

        if compression_info.overall_size_diff < 0:
            compression_info.overall_size_diff = \
                "expanded by " + str(abs(compression_info.overall_size_diff))
        # if the overall size difference is positive, it was compressed
        else:
            compression_info.overall_size_diff = \
                "compressed by " + str(compression_info.overall_size_diff)
        # add the overall compression stats to the compression info
        compression_info.add_info("OVERALL COMPRESSION STATS:",
                                  runtime, compression_info.overall_size_diff)
        # display the compression stats with GUI
        compression_info.compression_stats_gui()
        compression_info.reset()
        return result

    return wrapper


def calculate_overall_diff() -> float:
    """

    :return: The overall size difference.
    """
    original_size = compression_info.original_data_size
    print("archive path", compression_info.archive_path)
    print(type(compression_info.archive_path))
    print(f"Original size: {original_size}")
    print(f"arcihve size {Path(compression_info.archive_path).stat().st_size}")
    archive_size = Path(compression_info.archive_path).stat().st_size

    return original_size - archive_size
