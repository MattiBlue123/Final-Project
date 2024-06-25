import time
from pathlib import Path
from GUI import CompressionInfoGUI


class CompressionInfo:
    def __init__(self):
        self.files_compression_info = []
        self.overall_size_diff = 0

    def add_info(self, file_name, runtime, compressed_by):
        """
        :param file_name: name of the file and its parent directory
        :param runtime: runtime of the compression
        :param compressed_by: how much the file was compressed by
        :return:
        """
        self.files_compression_info.append((file_name, runtime, compressed_by))

    def compression_stats_gui(self):
        """
        The calling function for the CompressionInfoGUI
        :return:
        """
        gui = CompressionInfoGUI(self)
        gui.mainloop()

    def reset(self):
        """
        Resets the compression info between runs
        :return:
        """
        self.files_compression_info = []
        self.overall_size_diff = 0


compression_info = CompressionInfo()


def file_compressing_timer_decorator(func):
    """
    Decorator function to measure the time taken to compress a file and calculate the size difference before and after compression.

    :param func: The function to be decorated.
    :return: The decorated function.
    """

    def wrapper(self, metadata, pointer=0):
        """
        Wrapper function that is called instead of the decorated function.

        :param self: The instance of the class where the decorated function is defined.
        :param metadata: The metadata of the file to be compressed.
        :param pointer: The pointer to the current position in the file.
        :return: The result of the decorated function.
        """
        file_path = Path(metadata["origin path"])
        # not to be confused with two files with the same name in different directories
        file_name = f"{file_path.parent.name}/{file_path.stem}"
        start_time = time.time()
        result = func(self, metadata, pointer)
        end_time = time.time()
        runtime = end_time - start_time
        compressed_by = metadata["original size"] - metadata["encoded size"]
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


def archiving_timer_decorator(func):
    """
    Decorator function to measure the time taken to create an
    archive and calculate the overall size difference.

    :param func: The function to be decorated.
    :return: The decorated function.
    """

    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that is called instead of the decorated function.

        :param self: The instance of the class where the decorated function is defined.
        :param args: The positional arguments passed to the decorated function.
        :param kwargs: The keyword arguments passed to the decorated function.
        :return: The result of the decorated function.
        """
        start_time = time.time()
        result = func(self, *args, **kwargs)
        end_time = time.time()
        runtime = end_time - start_time
        # if the overall size difference is negative, the archive was expanded
        if compression_info.overall_size_diff > 0:
            compression_info.overall_size_diff = \
                "expanded by " + str(abs(compression_info.overall_size_diff))
        # if the overall size difference is positive, the archive was compressed
        else:
            compression_info.overall_size_diff = \
                "compressed by " + str(compression_info.overall_size_diff)
        # add the overall compression stats to the compression info
        compression_info.add_info("OVERALL COMPRESSION STATS:",
                                  runtime, compression_info.overall_size_diff)
        # display the compression stats withhey GUI
        compression_info.compression_stats_gui()
        compression_info.reset()
        return result

    return wrapper
