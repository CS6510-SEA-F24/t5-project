import os
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from src.tests.page import (
    MainPage,
    OutputPage,
)  # Ensure src.tests.page contains the correct MainPage and OutputPage


class PythonOrgSearch(unittest.TestCase):
    """A sample test class to show how page object works"""

    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(
            service=Service("/opt/homebrew/bin/geckodriver"), options=options
        )
        # Open the local HTML file
        self.file_path = "file:///Users/yoyowu/NEU/t5_grp/src/main/output.html"
        if not os.path.exists(self.file_path[7:]):
            print(f"Error: The file '{self.file_path}' does not exist.")
            self.fail(f"The file '{self.file_path}' does not exist.")

        self.driver.get(self.file_path)
        self.base_page = MainPage(self.driver)
        # Open the local HTML file

    def test_search_in_local_output_html(self):
        main_page = MainPage(self.driver)
        self.assertTrue(
            main_page.is_title_matches(),
            "Page title doesn't match."
        )

        pipeline_title = main_page.get_pipeline_title()
        self.assertTrue(pipeline_title, "Pipeline title is empty.")

        search_results_page = OutputPage(self.driver)
        self.assertTrue(
            search_results_page.is_pipeline_displayed(),
            "Pipeline is not displayed."
        )

    def tearDown(self):
        try:
            self.driver.close()
        except NoSuchWindowException:
            pass


if __name__ == "__main__":
    unittest.main()
