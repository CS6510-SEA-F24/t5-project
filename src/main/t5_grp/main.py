import os
import subprocess
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from .visualization import diagram_generator
import argparse
from .parser import yaml_parser
from .page import MainPage, OutputPage


def start_http_server(base_dir, port=8000):
    """
    Starts a simple HTTP server to serve content from a specified directory.

    Args:
        base_dir (str): The base directory for the project.
        port (int, optional): The port number for the HTTP server.
                            Default is 8000.

    Returns:
        subprocess.Popen: The process of the started server.
    """
    os.chdir(os.path.join(base_dir, 'src/main'))
    server = subprocess.Popen(['python', '-m', 'http.server', str(port)])
    time.sleep(2)
    return server


def open_browser(url, chrome_driver_path):
    """
    Uses Selenium to open a browser and verify specific web elements.

    Args:
        url (str): The URL to open in the browser.
        chrome_driver_path (str): The path to the ChromeDriver executable.
    """
    print(f"Using ChromeDriver at: {chrome_driver_path}")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = (
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    )
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # Optional: run in headless mode
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    # Wait for the page element to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    version = driver.capabilities['browserVersion']
    print(f"Chrome version: {version}")

    # Use page objects for operations
    main_page = MainPage(driver)
    output_page = OutputPage(driver)

    # Verify page title
    assert main_page.is_title_matches(), "Page title does not match."
    print(main_page.get_pipeline_title())

    # Verify if the pipeline is displayed
    assert output_page.is_pipeline_displayed(), "Pipeline is not displayed."

    input("Press Enter to close the browser...")
    driver.quit()


def main(yaml_file_path, base_dir, chrome_driver_path):
    """
    Main function to generate CI/CD pipeline visualization and open it in a
    browser.

    Args:
        yaml_file_path (str): Path to the YAML file.
        base_dir (str): The base directory for the project.
        chrome_driver_path (str): The path to the ChromeDriver executable.
    """
    try:
        data = yaml_parser.parse_yaml(yaml_file_path)
        if data is None:
            print("Failed to parse YAML file or validation error occurred.")
            return
        diagram_generator.generate_html(data)
        server = start_http_server(base_dir)
        open_browser('http://localhost:8000/output.html', chrome_driver_path)
        server.terminate()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def cli():
    """
    Command Line Interface (CLI) function to parse command line arguments and
    invoke the main function.
    """
    default_yaml = os.path.join(
        os.getcwd(),
        "src/tests/test_files/valid.yaml"  # Default YAML path
    )
    default_chrome = "/usr/local/bin/chromedriver"

    parser = argparse.ArgumentParser(
        description="Generate CI/CD pipeline visualization from YAML file."
    )
    parser.add_argument(
        "-y", "--yaml",
        default=default_yaml,
        help="Path to CI/CD config YAML file"
    )
    parser.add_argument(
        "-d", "--dir",
        default=os.getcwd(),
        help="Base directory for the project"
    )
    parser.add_argument(
        "-c", "--chrome",
        default=default_chrome,
        help="Path to the Chrome driver executable"
    )
    args = parser.parse_args()
    main(args.yaml, args.dir, args.chrome)


if __name__ == "__main__":
    cli()
