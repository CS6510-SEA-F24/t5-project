import os
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from src.tests.page import MainPage, OutputPage
import time


class PythonOrgSearch(unittest.TestCase):
    """Test class for verifying the local output HTML page."""

    def setUp(self):
        """Set up the test environment, including initializing the Chrome driver and loading the local HTML file."""
        options = Options()

        # Determine the appropriate ChromeDriver path based on the environment
        if os.environ.get('GITHUB_ACTIONS'):
            driver_path = "/usr/local/bin/chromedriver"
        else:
            driver_path = self.get_chromedriver_path()

        # Verify that the driver path is a valid executable file
        print(f"ChromeDriver path: {driver_path}")
        if not os.path.isfile(driver_path):
            raise ValueError(f"The path is not a valid file: {driver_path}")

        if not os.access(driver_path, os.X_OK):
            raise PermissionError(f"The path is not an executable file: {driver_path}")

        # Initialize the Chrome driver
        self.driver = webdriver.Chrome(service=Service(driver_path), options=options)

        # Open the local HTML file
        local_file_path = "file:///Users/yoyowu/NEU/t5_grp/src/main/output.html"
        self.driver.set_page_load_timeout(120)
        self.driver.get(local_file_path)

    def get_chromedriver_path(self):
        """Get the ChromeDriver path based on the operating system."""
        if os.name == 'nt':
            return "path/to/windows/chromedriver"
        elif os.name == 'posix':
            if os.environ.get('GITHUB_ACTIONS'):
                return "/usr/local/bin/chromedriver"
            else:
                return "/opt/homebrew/bin/chromedriver"
        else:
            raise RuntimeError("Unknown operating system")

    def test_search_in_local_output_html(self):
        """Test the search functionality in the local output HTML file."""
        main_page = MainPage(self.driver)

        # Check if the title matches the expected value
        self.assertTrue(main_page.is_title_matches(), "Page title doesn't match.")

        # Check if the pipeline title is present
        pipeline_title = main_page.get_pipeline_title()
        self.assertTrue(pipeline_title, "Pipeline title is empty.")

        # Check if the pipeline is displayed on the results page
        search_results_page = OutputPage(self.driver)
        self.assertTrue(search_results_page.is_pipeline_displayed(), "Pipeline is not displayed.")

        # Sleep to allow manual verification if needed
        time.sleep(3)

    def tearDown(self):
        """Clean up the test environment by closing the browser window."""
        try:
            self.driver.close()
        except NoSuchWindowException:
            pass


if __name__ == "__main__":
    unittest.main()
