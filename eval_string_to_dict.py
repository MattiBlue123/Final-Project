import re


class EvalStringToDict:
    """
    Mimics the functionality of libraries such as
    ast and JSON, but with a more restrictive input format.
    The input is a string that represents a dictionary as produced
    by the create_metadata_string method in the CompressionInit class.
    """

    def __init__(self, string_content):
        self.all_files_names = None
        self.string_content = string_content
        self.metadata = None

    @staticmethod
    def validate_string(input_string):
        """
        Validates that the string containing the metadata after the
        names of the files and folders have been removed, doesn't have
        potential security vulnerabilities that can be realized using the
        eval().
        :param input_string:
        :return: bool
        """
        if re.search(r'[^a-zA-Z0-9\'",:{}\s]', input_string):
            return False
        return True

    def process_string(self):
        """
        Processes the string content to replace the file names with a
        placeholder.
        It's essential to call this method before calling the eval()
        function to avoid security vulnerabilities.
        :return:
        """
        matches = re.findall(r'\|(.*?)\|', self.string_content)
        self.all_files_names = [(f"file {i + 1}", match) for i, match in
                                enumerate(matches)]
        for i, match in enumerate(matches):
            self.string_content = \
                self.string_content.replace(f"|{match}|", f"file {i + 1}")

    def restore_files_names(self, curr_dict):
        """
        Restores the files names (instead of the placeholders) in the metadata
        dictionary with the original names
        after the eval() function has been called.
        :param curr_dict: The metadata then it's nested dicts.
        :return: Updated metadata dictionary with original file names.
        """
        # Iterate over the key-value pairs in the metadata dictionary.
        for key, value in list(curr_dict.items()):
            # Check if the value is a dictionary.
            if isinstance(value, dict):
                # Iterate over the tuples in self.all_files_names.
                for i, (file_number, file_name) in enumerate(
                        self.all_files_names):
                    # If the key matches the file number in the tuple.
                    if key == file_number:
                        # Restore original name.
                        curr_dict[file_name] = curr_dict.pop(key)
                        # Remove the tuple from self.all_files_names.
                        self.all_files_names.pop(i)
                        # Recursively call the method for nested dictionaries.
                        curr_dict[file_name] = self.restore_files_names(value)
                        break
        # Return the updated metadata dictionary.
        return curr_dict





    def process_to_metadata(self):
        """
        :return: The string content as a dictionary of metadata
        """
        self.string_content.replace("'", '"')
        self.process_string()
        if not self.validate_string(self.string_content):
            return False
        try:
            self.metadata = eval(self.string_content)
        except Exception as e:
            print(f"Error processing string to metadata: {e}")
            return False
        self.metadata = self.restore_files_names(self.metadata)
        if self.all_files_names:
            print(f"Error processing string to metadata: invalid keys or "
                  f"values")
        return self.metadata



