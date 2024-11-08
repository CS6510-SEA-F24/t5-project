import unittest
from src.main.t5_grp.parser.yaml_parser import parse_yaml

"""
This module contains tests to validate the functionality of
the `parse_yaml` function,
ensuring it correctly parses valid YAML files and handles invalid YAML files.
Classes:
    TestYamlParser: Contains tests for the `parse_yaml` function.
Methods:
    test_valid_yaml:
        Tests if the `parse_yaml` function correctly parses a valid YAML file
        and returns the expected data.
    test_invalid_yaml:
        Tests if the `parse_yaml` function correctly handles an invalid case
        and returns None.
"""


class TestYamlParser(unittest.TestCase):
    """
    Contains unit tests for the `parse_yaml` function.
    The `parse_yaml` function behaves as expected for both valid
    and invalid YAML files.
    """

    def test_valid_yaml(self):
        """
        Tests the `parse_yaml` function with a valid YAML file.
        Ensures that the function correctly parses the file
        and the resulting data contains expected keys.
        """
        file_path = "src/tests/test_files/valid.yaml"
        result = parse_yaml(file_path)
        self.assertIsNotNone(result)
        self.assertIn("pipeline", result)

    def test_invalid_yaml(self):
        """
        Tests the `parse_yaml` function with an invalid YAML file.
        Ensures that the function returns None when the YAML file is invalid.
        """
        result = parse_yaml(
            "invalid.yaml"
        )  # Assuming invalid.yaml is an invalid YAML file
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
