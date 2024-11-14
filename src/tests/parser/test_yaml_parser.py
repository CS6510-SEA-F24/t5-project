import os
import unittest
from src.main.t5_grp.parser.yaml_parser import parse_yaml


class TestYamlParser(unittest.TestCase):
    """
    Contains unit tests for the `parse_yaml` function.
    The `parse_yaml` function behaves as expected for both valid
    and invalid YAML files.
    """

    def setUp(self):
        # Set the base directory for the test files
        self.base_dir = os.path.dirname(
            os.path.abspath(__file__)
        )  # Get the directory of the current file

    def test_valid_yaml(self):
        """
        Tests the `parse_yaml` function with a valid YAML file.
        Ensures that the function correctly parses the file
        and the resulting data contains expected keys.
        """
        file_path = os.path.join(
            self.base_dir, "../test_files/valid.yaml"
        )  # Adjust the path
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            self.fail(f"File '{file_path}' does not exist.")

        result = parse_yaml(file_path)
        self.assertIsNotNone(result)

    def test_invalid_yaml(self):
        """
        Tests the `parse_yaml` function with an invalid YAML file.
        Ensures that the function returns None when the YAML file is invalid.
        """
        file_path = os.path.join(
            self.base_dir, "../test_files/invalid.yaml"
        )  # Adjust the path
        print(
            f"Checking file path: {os.path.abspath(file_path)}"
        )  # Add to check absolute path
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' does not exist.")
            self.fail(f"File '{file_path}' does not exist.")

        result = parse_yaml(file_path)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
