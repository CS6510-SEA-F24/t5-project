import os
import argparse
from .parser import yaml_parser
from .visualization import diagram_generator
from .page import BasePage


def main(yaml_file_path, base_dir):
    """
    Main function to generate CI/CD pipeline visualization.

    Args:
        yaml_file_path (str): Path to the YAML file.
        base_dir (str): The base directory for the project.
    """
    try:
        data = yaml_parser.parse_yaml(yaml_file_path)
        if data is None:
            print("Failed to parse YAML file or validation error occurred.")
            return
        diagram_generator.generate_html(data)

        base_page = BasePage(None)
        server = base_page.start_http_server(base_dir)

        print("Server started.Open the visualization in your browser.")
        input("Press Enter to stop the server...")
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
    args = parser.parse_args()
    main(args.yaml, args.dir)


if __name__ == "__main__":
    cli()
