import unittest
from time import sleep
from selenium import webdriver
from t5_grp.page import MainPage, OutputPage


class PythonOrgSearch(unittest.TestCase):
    """A sample test class to show how page object works"""

    def setUp(self):
        self.driver = webdriver.Chrome()  # Changed to use Chrome
        self.driver.get("http://localhost:8000/output.html")

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
        sleep(3)
        search_results_page = OutputPage(self.driver)
        self.assertTrue(search_results_page.is_pipeline_displayed(),
                        "found pipeline.")

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
