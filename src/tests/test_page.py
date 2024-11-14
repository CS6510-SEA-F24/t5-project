
import os
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from src.tests.page import MainPage, OutputPage
import pytest
import time

@pytest.mark.browser
class PythonOrgSearch(unittest.TestCase):
    """Test class for verifying the local output HTML page."""

    def setUp(self):
        options = Options()
        driver_path = self.get_chromedriver_path()

        # Verify driver path
        print(f"ChromeDriver path: {driver_path}")
        if not os.path.isfile(driver_path):
            raise ValueError(f"The path is not a valid file: {driver_path}")

        if not os.access(driver_path, os.X_OK):
            raise PermissionError(f"The path is not an executable file: "
                                  f"{driver_path}")

        self.driver = webdriver.Chrome(service=Service(driver_path),
                                       options=options)

        # Open the local HTML file
        local_file_path ="file:///Users/yoyowu/NEU/t5_grp/src/main/output.html"
        self.driver.set_page_load_timeout(360)
        self.driver.get(local_file_path)

    def get_chromedriver_path(self):
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
        main_page = MainPage(self.driver)
        self.assertTrue(main_page.is_title_matches(),
                        "Page title doesn't match.")

        pipeline_title = main_page.get_pipeline_title()
        self.assertTrue(pipeline_title, "Pipeline title is empty.")

        search_results_page = OutputPage(self.driver)
        self.assertTrue(search_results_page.is_pipeline_displayed(),
                        "Pipeline is not displayed.")
        time.sleep(5)

    def tearDown(self):
        try:
            self.driver.close()
        except NoSuchWindowException:
            pass


if __name__ == "__main__":
    unittest.main()
