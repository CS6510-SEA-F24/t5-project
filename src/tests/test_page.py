import os
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from src.tests.page import MainPage, OutputPage


class PythonOrgSearch(unittest.TestCase):
    """Test class for verifying the local output HTML page."""

    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        driver_path = None
        if os.name == 'nt':
            driver_path = "path/to/windows/geckodriver"
        elif os.name == 'posix':
            if os.environ.get('GITHUB_ACTIONS'):
                driver_path = "/usr/local/bin/geckodriver"
            else:
                driver_path = "/opt/homebrew/bin/geckodriver"
        else:
            raise RuntimeError("Unknown operating system")

        if not os.path.isfile(driver_path):
            raise ValueError(f"The path is not a valid file: {driver_path}")

        self.driver = webdriver.Firefox(service=Service(driver_path),
                                        options=options)

        # Open the local HTML file
        self.file_path = "file:///Users/yoyowu/NEU/t5_grp/src/main/output.html"
        if not os.path.isfile(self.file_path[7:]):  # Check if the file exists
            raise FileNotFoundError(f"The file'{self.file_path}' not exist.")

        self.driver.get(self.file_path)
        self.base_page = MainPage(self.driver)

    def test_search_in_local_output_html(self):
        main_page = MainPage(self.driver)
        self.assertTrue(main_page.is_title_matches(),
                        "Page title doesn't match.")

        pipeline_title = main_page.get_pipeline_title()
        self.assertTrue(pipeline_title, "Pipeline title is empty.")

        search_results_page = OutputPage(self.driver)
        self.assertTrue(search_results_page.is_pipeline_displayed(),
                        "Pipeline is not displayed.")

    def tearDown(self):
        try:
            self.driver.close()
        except NoSuchWindowException:
            pass


if __name__ == "__main__":
    unittest.main()
