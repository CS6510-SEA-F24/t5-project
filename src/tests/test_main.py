import os
import unittest
from unittest.mock import patch
from src.main.t5_grp.main import main

"""
Unit tests for the main module.

This module contains tests to verify that the main function handles YAML
parsing and HTML generation correctly.

Classes:
    TestMainFunction: Tests for the main function.
"""


class TestMainFunction(unittest.TestCase):

    @patch("src.main.t5_grp.parser.yaml_parser.parse_yaml")
    @patch("src.main.t5_grp.visualization.diagram_generator.generate_html")
    def test_main(self, mock_generate_html, mock_parse_yaml):
        # Mock return value
        mock_parse_yaml.return_value = {"pipeline": {"name": "P1"}}

        # Create a temporary YAML file for testing
        test_yaml_path = "test.yaml"
        test_output_path = "output.html"
        with open(test_yaml_path, "w") as f:
            f.write("pipeline:\n  name: P1")

        try:
            # Call the main function with both paths
            main(test_yaml_path, output_path=test_output_path)

            # Verify parse_yaml was called
            mock_parse_yaml.assert_called_once_with(test_yaml_path)

            # Verify generate_html was called with correct arguments
            mock_generate_html.assert_called_once_with(
                {"pipeline": {"name": "P1"}}, output_path=test_output_path
            )

        finally:
            # Cleanup
            os.remove(test_yaml_path)


if __name__ == "__main__":
    unittest.main()
