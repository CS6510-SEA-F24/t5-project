"""
Page Object Model classes for Selenium WebDriver interactions.
This implements the Page Object pattern for the CI/CD pipeline
visualization web interface. It provides classes to encapsulate web
element interactions and verifications for different pages.
"""

from selenium.webdriver.common.by import By


class BasePage:
    """Base class for all page objects."""

    def __init__(self, driver):
        """
        Initialize base page with WebDriver instance.
        Args:
            driver: Selenium WebDriver instance for browser control.
        """
        self.driver = driver


class MainPage(BasePage):
    """Page object for the main pipeline visualization page."""

    def is_title_matches(self):
        """
        Check if page title contains expected pipeline name.
        Returns:
            bool: True if title contains 'P1', False otherwise.
        """
        return "P1" in self.driver.title

    def get_pipeline_title(self):
        """
        Get pipeline title from h1 element.
        Returns:
            str: Text content of the h1 element.
        """
        return self.driver.find_element(By.ID, "pipeline-title").text


class OutputPage(BasePage):
    """Page object for the pipeline output visualization."""

    def is_pipeline_displayed(self):
        """
        Check if pipeline visualization is present.
        Returns:
            bool: True if pipeline element exists, False otherwise.
        """
        return self.driver.find_element(By.CLASS_NAME, "pipeline") is not None
