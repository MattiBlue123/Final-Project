import time
from pathlib import Path


class CompressionInfo:
    def __init__(self):
        self.files_compression_info = []

    def add_info(self, file_name, runtime, compressed_by):
        self.files_compression_info.append((file_name, runtime, compressed_by))

    def print_info(self):
        for info in self.files_compression_info:
            print(f"File: {info[0]}, Compression Time: {info[1]} seconds, "
                  f"Compression Diff: {info[2]} bytes")


compression_info = CompressionInfo()


def timer_decorator(func):
    def wrapper(self, metadata, pointer=0):
        file_path = Path(metadata["origin path"])
        file_name = f"{file_path.parent.name}/{file_path.stem}"
        start_time = time.time()
        result = func(self, metadata, pointer)
        end_time = time.time()
        runtime = end_time - start_time
        # Calculate the "compressed_by" value
        compressed_by = metadata["original size"] - metadata["encoded size"]
        if compressed_by < 0:
            compressed_by = "expanded by " + str(abs(compressed_by))
        else:
            compressed_by = "compressed by " + str(compressed_by)
        # Append the file name, runtime, and "compressed_by" value to the list
        compression_info.add_info(file_name, runtime, compressed_by)
        return result

    return wrapper


def overall_timer_decorator(func):
    def wrapper(self, *args, **kwargs):
        start_time = time.time()
        result = func(self, *args, **kwargs)
        end_time = time.time()
        runtime = end_time - start_time

        # Add the overall compression runtime to the files_compression_info list
        compression_info.add_info("OVERALL COMPRESSION RUNTIME:", runtime, "")
        # compression_info.run_gui()
        return result

    return wrapper
