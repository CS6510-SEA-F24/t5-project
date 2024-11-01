import os


def check_file_exists(file_path):
    """
    Check if a file exists at the given path.

    Parameters:
        file_path (str): The path to the file to be checked.

    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.isfile(file_path)
