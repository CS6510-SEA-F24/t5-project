import os
import unittest
from unittest.mock import patch, MagicMock
from src.main.t5_grp.main import main

"""
Unit tests for the `main` function in the t5_grp.main module.
This module contains tests to verify that the main function handles YAML
parsing and HTML generation correctly by mocking all necessary dependencies.
"""


class TestMainFunction(unittest.TestCase):

    @patch("src.main.t5_grp.parser.yaml_parser.parse_yaml")
    @patch("src.main.t5_grp.visualization.diagram_generator.generate_html")
    @patch("src.main.t5_grp.main.start_http_server")
    @patch("src.main.t5_grp.main.open_browser")
    def test_main_success(self, mock_open_browser, mock_server,
                          mock_generate_html, mock_parse_yaml):
        # Mock return values
        mock_parse_yaml.return_value = {"pipeline": {"name": "P1"}}
        mock_server.return_value = MagicMock()

        # Test data
        test_yaml_path = "test.yaml"
        test_base_dir = os.getcwd()
        test_chrome_driver = "/usr/local/bin/chromedriver"

        with open(test_yaml_path, "w") as f:
            f.write("pipeline:\n  name: P1")

        try:
            # Call main with all required parameters
            main(test_yaml_path, test_base_dir, test_chrome_driver)

            # Verify all mocked functions were called correctly
            mock_parse_yaml.assert_called_once_with(test_yaml_path)
            mock_generate_html.assert_called_once_with(
                {"pipeline": {"name": "P1"}}
            )
            mock_server.assert_called_once_with(test_base_dir)
            mock_open_browser.assert_called_once_with(
                'http://localhost:8000/output.html',
                test_chrome_driver
            )
            mock_server.return_value.terminate.assert_called_once()

        finally:
            # Cleanup
            if os.path.exists(test_yaml_path):
                os.remove(test_yaml_path)

    @patch("src.main.t5_grp.parser.yaml_parser.parse_yaml")
    def test_main_parse_failure(self, mock_parse_yaml):
        # Mock parse_yaml to return None (indicating failure)
        mock_parse_yaml.return_value = None

        # Test data
        test_yaml_path = "test.yaml"
        test_base_dir = os.getcwd()
        test_chrome_driver = "/usr/local/bin/chromedriver"

        with open(test_yaml_path, "w") as f:
            f.write("invalid: yaml: content")

        try:
            # Call main and verify it handles the failure case
            main(test_yaml_path, test_base_dir, test_chrome_driver)
            mock_parse_yaml.assert_called_once_with(test_yaml_path)

        finally:
            if os.path.exists(test_yaml_path):
                os.remove(test_yaml_path)


if __name__ == "__main__":
    unittest.main()
