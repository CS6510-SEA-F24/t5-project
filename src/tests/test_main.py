import os
import unittest
from unittest.mock import patch
from src.main.t5_grp.main import main

"""
Unit tests for the `main` function in the t5_grp.main module.
This module contains tests to verify that the main function handles YAML
parsing and HTML generation correctly by mocking the
`yaml_parser.parse_yaml` and `diagram_generator.generate_html` functions.
Classes:
    TestMainFunction:
        Tests for the main function.
"""


class TestMainFunction(unittest.TestCase):

    @patch("src.main.t5_grp.parser.yaml_parser.parse_yaml")
    @patch("src.main.t5_grp.visualization.diagram_generator.generate_html")
    def test_main(self, mock_generate_html, mock_parse_yaml):
        # Mock return value
        mock_parse_yaml.return_value = {"pipeline": {"name": "P1"}}

        # Create a temporary YAML file for testing
        test_yaml_path = "test.yaml"
        with open(test_yaml_path, "w") as f:
            f.write("pipeline:\n  name: P1")

        try:
            # Call the main function with the path to the mock YAML file
            main(test_yaml_path)

            mock_parse_yaml.assert_called_once_with(test_yaml_path)
            mock_generate_html.assert_called_once()
        finally:
            # Cleanup: remove the temporary file
            os.remove(test_yaml_path)


if __name__ == "__main__":
    unittest.main()
