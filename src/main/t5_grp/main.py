from t5_grp.parser import yaml_parser
from t5_grp.visualization import diagram_generator
import argparse
"""
This module serves as the entry point for generating CI/CD pipeline visualizations from a YAML file.

Functions:
    main(yaml_file_path):
        Parses the YAML file and generates an HTML visualization if valid.

    cli():
        Sets up the command-line interface for the script.

Usage:
    Run the script from the command line with the path to the YAML file as an argument to generate the visualization.
"""
def main(yaml_file_path):
    """
    Parses the given YAML file and generates an HTML visualization.

    Args:
        yaml_file_path (str): Path to the YAML file containing the CI/CD configuration.

    This function uses the yaml_parser module to parse and validate the YAML file.
    If the YAML file is valid, it passes the data to the diagram_generator module to create the HTML visualization.
    """
    try:
        # Parse the YAML file and validate its content
        data = yaml_parser.parse_yaml(yaml_file_path)
        if data is None:
            print("Failed to parse YAML file or validation error occurred.")
            return
        # Generate the HTML visualization from the parsed data
        diagram_generator.generate_html(data)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def cli():
    """
    Sets up the command-line interface for the script.

    This function defines the command-line arguments and passes them to the main function.
    It expects one argument: the path to the CI/CD configuration YAML file.
    """
    # Create the parser with a description
    parser = argparse.ArgumentParser(description="Generate CI/CD pipeline visualization from YAML file.")
    parser.add_argument("yaml_file", help="Path to the CI/CD configuration YAML file.")
    # Parse the arguments and call the main function with the YAML file path
    args = parser.parse_args()
    main(args.yaml_file)

if __name__ == "__main__":
    cli()