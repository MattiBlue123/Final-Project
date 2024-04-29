def find_largest_pointer(metadata_dict=None, largest_pointer=0):
    if metadata_dict is None:
        metadata_dict = archive_metadata

    for key, value in metadata_dict.items():
        if isinstance(value, dict):
            if "pointer" in value.keys() and isinstance(value["pointer"],
                                                        int):
                if value["pointer"] > largest_pointer:
                    largest_pointer = value["pointer"]
            largest_pointer = find_largest_pointer(value,
                                                        largest_pointer)

    return largest_pointer



archive_metadata = {
    "file1": {
        "pointer": 1,
        "size": 100,
        "nested_file": {
            "pointer": 2,
            "size": 50
        }
    },
    "file2": {
        "pointer": 11,
        "size": 200,
        "nested_file": {
            "pointer": 94,
            "size": 75,
            "double_nested_file": {
                "pointer": 5,
                "size": 25
            }
        }
    },
    "file3": {
        "pointer": 6,
        "size": 300
    }
}


def get_relevant_metadata():
    path = parse_archive_path(archive_path)
    current_dict = archive_metadata
    for key in path:
        if key in current_dict and isinstance(current_dict[key], dict):
            current_dict = current_dict[key]
        else:
            return False
    return current_dict

def parse_archive_path(archive_path):
    # Remove leading and trailing slashes
    archive_path = archive_path.strip('/')
    # Split the path into a list of files/directories
    files = archive_path.split('/')
    return files


archive_path = "/file2/nested_file"

print(get_relevant_metadata())