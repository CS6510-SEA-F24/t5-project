
import unittest
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from t5_grp.page import MainPage, OutputPage


class PythonOrgSearch(unittest.TestCase):
    """A sample test class to show how page object works"""

    def setUp(self):
        self.driver = webdriver.Chrome()  # Changed to use Chrome
        self.base_page = MainPage(self.driver)
        self.server = self.base_page.start_http_server(base_dir='/Users/yoyowu/NEU/t5_grp')
        try:
            self.driver.get("http://localhost:8000/output.html")
        except WebDriverException as e:
            self.driver.quit()
            self.base_page.stop_http_server()
            raise RuntimeError("Unable to access the local server. Please ensure the server is running and accessible at 'http://localhost:8000/output.html'") from e

    def test_search_in_python_org(self):
        """
        Tests python.org search feature. Searches for the word "pycon" then
        verifies that some results show up. Note that it does not look for
        any particular text in search results page. This test verifies that
        the results were not empty.
        """
        main_page = MainPage(self.driver)
        self.assertTrue(main_page.is_title_matches(),
                        "python.org title doesn't match.")
        sleep(2)

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
        self.base_page.stop_http_server()


if __name__ == "__main__":
    unittest.main()
