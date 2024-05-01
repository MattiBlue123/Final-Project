import time
from pathlib import Path

class CompressionInfo:
    def __init__(self):
        self.files_compression_info = []

    def add_info(self, file_name, runtime):
        self.files_compression_info.append((file_name, runtime))

    def print_info(self):
        for info in self.files_compression_info:
            print(f"File: {info[0]}, Runtime: {info[1]} seconds")

compression_info = CompressionInfo()

def timer_decorator(func):
    def wrapper(self, metadata, pointer=0):
        file_path = Path(metadata["origin path"])
        file_name = f"{file_path.parent.name}/{file_path.stem}"
        start_time = time.time()
        result = func(self, metadata, pointer)
        end_time = time.time()
        runtime = end_time - start_time
        # Append the file name and runtime to the list
        compression_info.add_info(file_name, runtime)
        return result
    return wrapper