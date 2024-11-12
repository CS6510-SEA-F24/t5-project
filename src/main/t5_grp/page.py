# src/main/t5_grp/page.py

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

class MainPage(BasePage):
    def is_title_matches(self):
        return "P1" in self.driver.title

    def get_pipeline_title(self):
        return self.driver.find_element(By.TAG_NAME, "h1").text

class OutputPage(BasePage):
    def is_pipeline_displayed(self):
        return self.driver.find_element(By.CLASS_NAME, "pipeline") is not None