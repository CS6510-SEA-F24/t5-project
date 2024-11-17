import os
import unittest
from unittest.mock import patch, MagicMock
from src.main.t5_grp.visualization.diagram_generator import (
    generate_html,
    extract_pipeline_data,
    add_job_info,
)


class TestDiagramGenerator(unittest.TestCase):
    """
    Test suite for the diagram_generator module.

    This class contains unit tests for the functions in the diagram_generator
    module, including generate_html, extract_pipeline_data, and add_job_info.
    """

    @patch("src.main.t5_grp.visualization.diagram_generator.Environment")
    @patch("src.main.t5_grp.visualization.diagram_generator.os.path.exists")
    @patch("src.main.t5_grp.visualization.diagram_generator.os.makedirs")
    @patch(
        "src.main.t5_grp.visualization.diagram_generator.open",
        new_callable=unittest.mock.mock_open,
    )
    def test_generate_html(
        self, mock_open, mock_makedirs, mock_exists, mock_environment
    ):
        """
        Test the generate_html function.

        This test verifies that the generate_html function correctly creates
        an HTML file from the provided pipeline data. It mocks the necessary
        components to ensure that the function behaves as expected without
        actually creating files or directories.

        Asserts that:
        - The output directory is created if it does not exist.
        - The HTML file is opened for writing with the correct path.
        - The rendered HTML content is written to the file.
        """
        # Arrange
        mock_exists.return_value = False
        mock_template = MagicMock()
        mock_environment.return_value.get_template.return_value = mock_template
        mock_template.render.return_value = "<html></html>"

        data = {
            "pipeline": {"name": "Test Pipeline"},
            "stages": ["build", "test"],
            "jobs": [],
        }
        # Define test output directory
        output_dir = "/test/output/dir"
        output_path = os.path.join(output_dir, "output.html")

        # Act
        generate_html(data, output_dir)

        # Assert
        mock_exists.assert_called_once_with(output_dir)
        mock_makedirs.assert_called_once_with(output_dir)
        mock_open.assert_called_once_with(output_path, "w")
        mock_open().write.assert_called_once_with("<html></html>")

    def test_extract_pipeline_data(self):
        """
        Test the extract_pipeline_data function.

        This test verifies that the extract_pipeline_data function correctly
        extracts and organizes pipeline data from the provided YAML data.

        Asserts that:
        - The pipeline name is correctly extracted.
        - The jobs are included in the output.
        - The dependencies are correctly established based on job needs.
        """
        # Arrange
        data = {
            "pipeline": {"name": "Test Pipeline"},
            "stages": ["build", "test"],
            "jobs": [
                {
                    "name": "job1",
                    "stage": "build",
                    "needs": [],
                    "artifacts": {"paths": []},
                },
                {
                    "name": "job2",
                    "stage": "test",
                    "needs": ["job1"],
                    "artifacts": {"paths": []},
                },
            ],
        }

        # Act
        result = extract_pipeline_data(data)

        # Assert
        self.assertEqual(result["name"], "Test Pipeline")
        self.assertIn("job1", result["jobs"])
        self.assertIn("job2", result["jobs"])
        self.assertEqual(
            result["dependencies"],
            [
                {
                    "from": "job_job1",
                    "to": "job_job2",
                    "fromStage": "build",
                    "toStage": "test",
                }
            ],
        )

    def test_add_job_info(self):
        """
        Test the add_job_info function.

        This test verifies that the add_job_info function correctly adds job
        information to the pipeline data structure.

        Asserts that:
        - The job is added to the pipeline information.
        - The job's stage is correctly set.
        - No dependencies are added if there are none.
        """
        # Arrange
        pip_info = {
            "jobs": {},
            "dependencies": [],
            "stages": [{"name": "build", "artifacts": []}],
            "artifacts": {},
            "all_artifacts": [],
        }
        job = {
            "name": "job1",
            "stage": "build",
            "needs": [],
            "allow_failure": False,
            "artifacts": {"paths": []},
        }
        stage_artifacts = {}
        all_artifacts = set()

        add_job_info(pip_info, job, "job1", "build", stage_artifacts, all_artifacts)
        # Assert
        self.assertIn("job1", pip_info["jobs"])
        self.assertEqual(pip_info["jobs"]["job1"]["stage"], "build")
        self.assertEqual(pip_info["dependencies"], [])
        self.assertEqual(pip_info["jobs"]["job1"]["dependency_count"], 0)
        self.assertEqual(pip_info["jobs"]["job1"]["position"], 0)


if __name__ == "__main__":
    unittest.main()
