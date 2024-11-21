import os
import unittest
from unittest.mock import patch
from t5_grp.main import main


class TestMainFunction(unittest.TestCase):

    @patch("t5_grp.parser.yaml_parser.parse_yaml")
    @patch("t5_grp.visualization.diagram_generator.generate_html")
    def test_main(self, mock_generate_html, mock_parse_yaml):
        # Mock return value
        mock_parse_yaml.return_value = {
            "pipeline": {"name": "P1"},
            "__file__": "test.yaml",
        }

        # Create a temporary YAML file for testing
        test_yaml_path = "test.yaml"
        test_output_path = "output.html"
        test_theme = "light"
        test_stage_gap = 60

        with open(test_yaml_path, "w") as f:
            f.write("pipeline:\n  name: P1")

        try:
            # Call the main function with all parameters
            main(
                test_yaml_path,
                output_path=test_output_path,
                theme=test_theme,
                stage_gap=test_stage_gap,
            )

            # Verify parse_yaml was called
            mock_parse_yaml.assert_called_once_with(test_yaml_path)

            # Verify generate_html was called with correct arguments
            mock_generate_html.assert_called_once_with(
                {"pipeline": {"name": "P1"}, "__file__": "test.yaml"},
                output_path=test_output_path,
                theme=test_theme,
                stage_gap=test_stage_gap,
            )

        finally:
            # Cleanup
            os.remove(test_yaml_path)


if __name__ == "__main__":
    unittest.main()
