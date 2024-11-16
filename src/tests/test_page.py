import os
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from t5_grp.main import main
from page import MainPage, OutputPage
from selenium.webdriver.support.ui import WebDriverWait


class PythonOrgSearch(unittest.TestCase):
    """Test class for verifying the local output HTML page."""

    def setUp(self):
        """
        Set up test environment before executing tests.

        Steps:
        1. Generate the output.html using the main function.
        2. Set up Selenium WebDriver with required options.
        3. Load the generated output.html to test.
        """
        # Step 1: Generate the output.html first
        test_yaml_path = os.path.join(
            os.path.dirname(__file__), "test_files", "valid.yaml"
        )
        main(test_yaml_path)

        # Step 2: Set up Selenium WebDriver
        options = Options()
        if os.environ.get("GITHUB_ACTIONS"):
            options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver_path = self.get_chromedriver_path()

        if not os.path.isfile(driver_path):
            raise ValueError(f"The path is not a valid file: {driver_path}")

        if not os.access(driver_path, os.X_OK):
            raise PermissionError(
                f"The path is not an executable file: " f"{driver_path}"
            )
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        # Step 3: Find and load the generated output.html
        if os.environ.get("GITHUB_WORKSPACE"):
            workspace = os.environ.get("GITHUB_WORKSPACE")
            base_dir = os.path.join(workspace, "src", "main")
        else:
            base_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "src",
                "main",
            )

        local_file_path = os.path.join(base_dir, "output.html")

        if not os.path.exists(local_file_path):
            raise FileNotFoundError(
                f"The specified HTML file does not exist: {local_file_path}\n"
                f"Current directory: {os.getcwd()}\n"
                f"Directory contents: "
                f"{os.listdir(os.path.dirname(local_file_path))}"
            )

        self.driver.set_page_load_timeout(360)
        self.driver.get("file://" + local_file_path)

    def get_chromedriver_path(self):
        """
        Get the path to the ChromeDriver based on the environment.

        Returns:
            str: The path to the ChromeDriver executable.
        """
        if os.environ.get("GITHUB_ACTIONS"):
            default_path = "/usr/local/bin/chromedriver"
            return os.environ.get("CHROMEDRIVER_PATH", default_path)
        elif os.name == "nt":
            return "path/to/windows/chromedriver"
        else:
            return "/opt/homebrew/bin/chromedriver"

    def test_search_in_local_output_html(self):
        """
        Verify the content of the local output HTML page.

        Checks:
        1. The title of the main page matches the expected value.
        2. The pipeline title is present on the main page.
        3. The pipeline is displayed on the output page.
        """
        main_page = MainPage(self.driver)
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: driver.title)
        self.assertTrue(main_page.is_title_matches(),
                        "Page title doesn't match.")
        pipeline_title = main_page.get_pipeline_title()
        self.assertTrue(pipeline_title, "Pipeline title is empty.")
        search_results_page = OutputPage(self.driver)
        self.assertTrue(
            search_results_page.is_pipeline_displayed(),
            "Pipeline is not displayed."
        )

    def tearDown(self):
        """
        Clean up after tests; close the browser.
        """
        try:
            self.driver.close()
        except NoSuchWindowException:
            pass


if __name__ == "__main__":
    unittest.main()
