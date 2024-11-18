from .visualization import diagram_generator
import argparse
from .parser import yaml_parser

"""
This serves as the entry point for generating CI/CD pipeline visualizations
from a YAML file.

Functions:
    main(yaml_file_path):
        Parses the YAML file and generates an HTML visualization if valid.
    cli():
        Sets up the command-line interface for the script.

Usage:
    Run the script from the command line with the path to the YAML file as
    an argument to generate the visualization.
"""


def main(yaml_file_path, output_path="output.html"):
    """
    Parses the given YAML file and generates an HTML visualization.

    Args:
        yaml_file_path (str): Path to the YAML file containing the CI/CD configuration.
        output_path (str): Path where the HTML visualization will be generated.
    """
    try:
        # Parse the YAML file and validate its content
        data = yaml_parser.parse_yaml(yaml_file_path)
        if data is None:
            print("Failed to parse YAML file or validation error occurred.")
            return

        # Generate the HTML visualization with output path
        diagram_generator.generate_html(data, output_path=output_path)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def cli():
    """Sets up the command-line interface for the script."""
    parser = argparse.ArgumentParser(
        description="Generate CI/CD pipeline visualization from YAML file."
    )
    parser.add_argument("yaml_file", help="Path to CI/CD config YAML file.")
    parser.add_argument(
        "-o",
        "--output",
        default="output.html",
        help="Path for the generated HTML visualization (default: output.html)",
    )
    args = parser.parse_args()
    main(args.yaml_file, output_path=args.output)


if __name__ == "__main__":
    cli()
