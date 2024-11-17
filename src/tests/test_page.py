import unittest
import os
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

from tests.page.page import PipelinePage


class PipelinePageTest(unittest.TestCase):
    """Test class for pipeline visualization page.
    Tests the functionality of pipeline structure, stages,
    jobs, and their relationships."""

    def setUp(self):
        """Set up test environment before each test.
        Initializes Chrome WebDriver in headless mode
        and loads the pipeline HTML page."""
        try:
            # Configure Chrome options for running in CI/GitHub Actions environment:
            # --no-sandbox: Disable the sandbox for running in CI environment
            # --headless: Run Chrome in headless mode (without GUI)
            # --disable-dev-shm-usage: Overcome limited resource issues in CI containers
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")

            self.driver = webdriver.Chrome(options=chrome_options)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            html_path = os.path.join(current_dir, "..", "main", "output.html")
            file_url = f"file://{os.path.abspath(html_path)}"

            self.driver.get(file_url)
            self.pipeline_page = PipelinePage(self.driver)
        except WebDriverException as e:
            self.fail(f"Failed to setup test environment: {str(e)}")

    def test_pipeline_structure(self):
        """Test if pipeline structure is valid"""
        result = self.pipeline_page.verify_pipeline_structure()
        self.assertTrue(
            result.success, f"Pipeline structure verification failed: {result.message}"
        )

    def test_pipeline_name(self):
        """Test if pipeline name is correct"""
        name = self.pipeline_page.get_pipeline_name()
        self.assertIsNotNone(name, "Pipeline name should not be None")
        self.assertEqual(name, "P1", "Pipeline name should be 'P1'")

    def test_pipeline_stages(self):
        """Test if pipeline stages are correct"""
        expected_stages = ["build", "test", "doc", "deploy"]
        stages = self.pipeline_page.get_stages()
        self.assertEqual(
            stages,
            expected_stages,
            f"Expected stages {expected_stages}, but got {stages}",
        )

    def test_stage_artifacts(self):
        """Test stage artifacts"""
        test_cases = {
            "build": ["build/classes/*", "build/reports/*"],
            "test": ["final.jar"],
            "deploy": ["distribution.tgz", "md5.sum"],
        }

        for stage, expected in test_cases.items():
            with self.subTest(stage=stage):
                artifacts = self.pipeline_page.get_stage_artifacts(stage)
                self.assertEqual(
                    artifacts, expected, f"Stage {stage} artifacts mismatch"
                )

    def test_job_dependencies(self) -> None:
        """Test job dependencies in the pipeline.
        Verifies that:
        1. Jobs without dependencies are correctly identified
        2. Jobs with dependencies have correct dependency relationships
        3. Dependency chains are properly maintained
        """
        test_cases = {
            "compile": ["static_analysis"],
            "static_analysis": [],
            "unit_test": ["compile"],
            "generate_docs": ["unit_test"],
            "publish": ["generate_docs"],
        }

        no_deps_jobs = [job for job, deps in test_cases.items() if not deps]
        for job in no_deps_jobs:
            with self.subTest(job=job):
                deps = self.pipeline_page.get_job_dependencies(job)
                self.assertEqual(deps, [], f"Job {job} should have no dependencies")

        has_deps_jobs = [job for job, deps in test_cases.items() if deps]
        for job in has_deps_jobs:
            with self.subTest(job=job):
                deps = self.pipeline_page.get_job_dependencies(job)
                self.assertEqual(
                    sorted(deps),
                    sorted(test_cases[job]),
                    f"Job {job} dependencies mismatch: "
                    f"expected {test_cases[job]}, got {deps}",
                )

    def test_job_properties(self):
        """Test allow_failure property"""
        self.assertTrue(
            self.pipeline_page.is_job_allow_failure("static_analysis"),
            "static_analysis should allow failure",
        )
        self.assertFalse(
            self.pipeline_page.is_job_allow_failure("compile"),
            "compile should not allow failure",
        )

    def test_complete_pipeline_data(self):
        """Test complete pipeline data structure"""
        pipeline_data = self.pipeline_page.get_pipeline_data()
        self.assertIsNotNone(pipeline_data, "Pipeline data should not be None")

        # Verify basic structure
        self.assertEqual(pipeline_data.name, "P1")
        self.assertEqual(len(pipeline_data.stages), 4)

        # Verify all artifacts
        expected_artifacts = [
            "build/classes/*",
            "build/reports/*",
            "distribution.tgz",
            "final.jar",
            "md5.sum",
        ]
        self.assertEqual(
            sorted(pipeline_data.all_artifacts), sorted(expected_artifacts)
        )

    def tearDown(self):
        """Clean up after each test"""
        if hasattr(self, "driver"):
            try:
                self.driver.quit()
            except WebDriverException:
                pass


if __name__ == "__main__":
    unittest.main()
