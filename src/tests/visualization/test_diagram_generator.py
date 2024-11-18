import os
import tempfile
import unittest

from src.main.t5_grp.visualization.diagram_generator import (
    add_job_info,
    generate_html,
    extract_pipeline_data,
)
from t5_grp.config import PROJECT_ROOT, ASSETS_FOLDER, ASSET_FILES, TEST_OUTPUT_FILENAME


class TestDiagramGenerator(unittest.TestCase):
    """
    Test suite for the diagram_generator module.
    """

    def test_generate_html(self):
        """Test the generate_html function"""
        # Create a temporary directory for test output
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, TEST_OUTPUT_FILENAME)
            test_data = {
                "pipeline": {
                    "name": "Test Pipeline",
                    "stages": ["build", "test"],
                    "jobs": {
                        "job1": {"stage": "build"},
                        "job2": {"stage": "test", "needs": ["job1"]},
                    },
                }
            }

            # Call generate_html
            generate_html(test_data, output_path)

            # Verify output file exists
            self.assertTrue(os.path.exists(output_path))

            # Verify assets were copied
            assets_dir = os.path.join(temp_dir, PROJECT_ROOT, ASSETS_FOLDER)
            self.assertTrue(os.path.exists(assets_dir))
            for asset in ASSET_FILES:
                self.assertTrue(
                    os.path.exists(os.path.join(assets_dir, asset)),
                    f"Asset {asset} should exist",
                )

    def setUp(self):
        """Initialize variables that need to be reused in multiple test cases"""
        self.pip_info = {
            "jobs": {},
            "dependencies": [],
            "stages": [{"name": "test_stage", "artifacts": []}],
            "artifacts": {},
            "all_artifacts": [],
        }
        self.stage_artifacts = {}
        self.all_artifacts = set()

    def test_add_job_info(self):
        """
        Test the add_job_info function with different dependency scenarios.

        Tests the following cases:
        1. Job with no dependencies and not depended on (priority 0)
        2. Job with no dependencies but is depended on (priority 1)
        3. Job with dependencies and is depended on (priority 2)
        4. Job with dependencies but not depended on (priority 3)
        """
        # Case 1: Job with no dependencies and not depended on (priority 0)
        job1 = {"name": "job1", "stage": "test_stage", "needs": []}
        add_job_info(
            self.pip_info,
            job1,
            "job1",
            "test_stage",
            self.stage_artifacts,
            self.all_artifacts,
        )
        self.assertEqual(
            self.pip_info["jobs"]["job1"]["dependency_count"],
            0,
            "Job with no dependencies should have priority 0",
        )

        # Case 2: Job with no dependencies but is depended on (priority 1)
        job2 = {"name": "job2", "stage": "test_stage", "needs": []}
        add_job_info(
            self.pip_info,
            job2,
            "job2",
            "test_stage",
            self.stage_artifacts,
            self.all_artifacts,
        )
        # Add a job that depends on job2
        job3 = {"name": "job3", "stage": "test_stage", "needs": ["job2"]}
        add_job_info(
            self.pip_info,
            job3,
            "job3",
            "test_stage",
            self.stage_artifacts,
            self.all_artifacts,
        )
        self.assertEqual(
            self.pip_info["jobs"]["job2"]["dependency_count"],
            1,
            "Job that is depended on should have priority 1",
        )

        # Case 3: Job with dependencies and being depended on (priority 2)
        job4 = {"name": "job4", "stage": "test_stage", "needs": ["job1"]}
        add_job_info(
            self.pip_info,
            job4,
            "job4",
            "test_stage",
            self.stage_artifacts,
            self.all_artifacts,
        )
        # Add a job that depends on job4
        job5 = {"name": "job5", "stage": "test_stage", "needs": ["job4"]}
        add_job_info(
            self.pip_info,
            job5,
            "job5",
            "test_stage",
            self.stage_artifacts,
            self.all_artifacts,
        )
        self.assertEqual(
            self.pip_info["jobs"]["job4"]["dependency_count"],
            2,
            "Job with dependencies and being depended on should have priority 2",
        )

        # Case 4: Job with dependencies but not depended on (priority 3)
        job6 = {"name": "job6", "stage": "test_stage", "needs": ["job2"]}
        add_job_info(
            self.pip_info,
            job6,
            "job6",
            "test_stage",
            self.stage_artifacts,
            self.all_artifacts,
        )
        self.assertEqual(
            self.pip_info["jobs"]["job6"]["dependency_count"],
            3,
            "Job that only depends on others should have priority 3",
        )

        # Test correctness of dependencies
        self.assertIn(
            {
                "from": "job_job2",
                "to": "job_job6",
                "fromStage": "test_stage",
                "toStage": "test_stage",
            },
            self.pip_info["dependencies"],
            "Dependencies should be correctly recorded",
        )

        # Test artifacts processing
        job_with_artifacts = {
            "name": "job_artifacts",
            "stage": "test_stage",
            "artifacts": {"paths": ["test.txt", "report.pdf"]},
        }
        add_job_info(
            self.pip_info,
            job_with_artifacts,
            "job_artifacts",
            "test_stage",
            self.stage_artifacts,
            self.all_artifacts,
        )
        self.assertEqual(
            self.stage_artifacts["test_stage"],
            {"test.txt", "report.pdf"},
            "Stage artifacts should be correctly recorded",
        )
        self.assertTrue(
            {"test.txt", "report.pdf"}.issubset(self.all_artifacts),
            "All artifacts should be correctly recorded",
        )

    def test_extract_pipeline_data(self):
        test_data = {
            "pipeline": {"name": "Test Pipeline"},
            "stages": ["build", "test"],
            "jobs": [
                {
                    "name": "build_job",
                    "stage": "build",
                    "artifacts": {"paths": ["build.txt"]},
                },
                {"name": "test_job", "stage": "test", "needs": ["build_job"]},
            ],
        }

        result = extract_pipeline_data(test_data)

        self.assertEqual(result["name"], "Test Pipeline")
        self.assertEqual(len(result["stages"]), 2)
        self.assertEqual(len(result["jobs"]), 2)
        self.assertIn("build_job", result["jobs"])
        self.assertIn("test_job", result["jobs"])


if __name__ == "__main__":
    unittest.main()
