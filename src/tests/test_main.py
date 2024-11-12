import os
import unittest
from unittest.mock import patch, MagicMock
from src.main.t5_grp.main import main

"""
Unit tests for the `main` function in the t5_grp.main module.
This module contains tests to verify that the main function handles YAML
parsing and HTML generation correctly by mocking the
`yaml_parser.parse_yaml`, `diagram_generator.generate_html`,
and `BasePage.start_http_server` functions.
Classes:
    TestMainFunction:
        Tests for the main function.
"""


class TestMainFunction(unittest.TestCase):

    @patch("src.main.t5_grp.parser.yaml_parser.parse_yaml")
    @patch("src.main.t5_grp.visualization.diagram_generator.generate_html")
    @patch("src.main.t5_grp.page.BasePage.start_http_server")
    def test_main(self, mock_start_http_server, mock_generate_html,
                  mock_parse_yaml):
        # Mock return values
        mock_parse_yaml.return_value = {"pipeline": {"name": "P1"}}
        mock_start_http_server.return_value = MagicMock()

        # Create a temporary YAML file for testing
        test_yaml_path = "test.yaml"
        with open(test_yaml_path, "w") as f:
            f.write("pipeline:\n  name: P1")

        try:
            # Call the main function with the path to the mock YAML file
            # and a mock base directory
            main(test_yaml_path, os.getcwd())

            mock_parse_yaml.assert_called_once_with(test_yaml_path)
            mock_generate_html.assert_called_once()
            mock_start_http_server.assert_called_once_with(os.getcwd())
        finally:
            # Cleanup: remove the temporary file
            os.remove(test_yaml_path)


if __name__ == "__main__":
    unittest.main()
