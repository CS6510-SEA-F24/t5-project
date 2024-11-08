import unittest
from unittest.mock import patch
from t5_grp.main import main

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

    @patch("t5_grp.parser.yaml_parser.parse_yaml")
    @patch("t5_grp.visualization.diagram_generator.generate_html")
    def test_main(self, mock_generate_html, mock_parse_yaml):
        mock_parse_yaml.return_value = {"pipeline": {"name": "P1"}}
        main("test.yaml")
        mock_parse_yaml.assert_called_once_with("test.yaml")
        mock_generate_html.assert_called_once()


if __name__ == "__main__":
    unittest.main()
