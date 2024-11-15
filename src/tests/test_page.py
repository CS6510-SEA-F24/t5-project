import os
import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from t5_grp.main import main
from page import MainPage, OutputPage


class PythonOrgSearch(unittest.TestCase):
    """Test class for verifying the local output HTML page."""

    def setUp(self):
        # Step 1: Generate the output.html first
        test_yaml_path = os.path.join(os.path.dirname(__file__), "test_files", "valid.yaml")
        main(test_yaml_path)

        # Step 2: Set up Selenium WebDriver
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver_path = self.get_chromedriver_path()

        print(f"ChromeDriver path: {driver_path}")
        if not os.path.isfile(driver_path):
            raise ValueError(f"The path is not a valid file: {driver_path}")

        if not os.access(driver_path, os.X_OK):
            raise PermissionError(f"The path is not an executable file: {driver_path}")

        self.driver = webdriver.Chrome(service=Service(driver_path), options=options)

        # Step 3: Find and load the generated output.html
        if os.environ.get('GITHUB_WORKSPACE'):
            base_dir = os.path.join(os.environ.get('GITHUB_WORKSPACE'), 'src', 'main')
        else:
            base_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'src', 'main'
            )

        local_file_path = os.path.join(base_dir, "output.html")
        print(f"Looking for output.html at: {local_file_path}")

        if not os.path.exists(local_file_path):
            raise FileNotFoundError(
                f"The specified HTML file does not exist: {local_file_path}\n"
                f"Current directory: {os.getcwd()}\n"
                f"Directory contents: {os.listdir(os.path.dirname(local_file_path))}"
            )

        self.driver.set_page_load_timeout(360)
        self.driver.get("file://" + local_file_path)

    def get_chromedriver_path(self):
        if os.environ.get('GITHUB_ACTIONS'):
            return os.environ.get('CHROMEDRIVER_PATH', "/usr/local/bin/chromedriver")
        elif os.name == 'nt':
            return "path/to/windows/chromedriver"
        else:
            return "/opt/homebrew/bin/chromedriver"

    def test_search_in_local_output_html(self):
        main_page = MainPage(self.driver)
        self.assertTrue(main_page.is_title_matches(),
                        "Page title doesn't match.")

        pipeline_title = main_page.get_pipeline_title()
        self.assertTrue(pipeline_title, "Pipeline title is empty.")

        search_results_page = OutputPage(self.driver)
        self.assertTrue(search_results_page.is_pipeline_displayed(),
                        "Pipeline is not displayed.")
        time.sleep(3)

    def tearDown(self):
        try:
            self.driver.close()
        except NoSuchWindowException:
            pass


if __name__ == "__main__":
    unittest.main()
