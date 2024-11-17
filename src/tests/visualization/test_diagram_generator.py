import unittest

from src.main.t5_grp.visualization.diagram_generator import (
    add_job_info,
)


class TestDiagramGenerator(unittest.TestCase):
    """
    Test suite for the diagram_generator module.
    """

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


if __name__ == "__main__":
    unittest.main()
