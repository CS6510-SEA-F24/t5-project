import argparse
import os

from .parser.yaml_parser import parse_yaml, load_yaml_from_dry_run, check_file_exists
from .visualization.diagram_generator import generate_dot_diagram


def main():
    """
    Main function to generate a pipeline diagram from a given YAML file.

    This function performs the following steps:
    1. Parses command line arguments to get the file path of the YAML file.
    2. Checks if the provided file path exists.
    3. Parses the YAML file to extract pipeline data.
    4. Generates a DOT diagram from the extracted pipeline data.
    5. Prints the DOT source code.
    6. Renders the diagram to a PNG file and opens it for viewing.

    Usage:
        python main.py path/to/your/file.yaml

    Command Line Arguments:
        file_path (str): Path to the YAML file.
    """
    parser = argparse.ArgumentParser(description='Generate Pipeline Diagram from YAML')
    parser.add_argument('file_path', type=str, help='Path to the YAML file')
    parser.add_argument('--dry-run-command', type=str, nargs='?', help='CI/CD command to run with --dry-run')
    args = parser.parse_args()

    # Check if the file path is provided and the file exists
    if args.file_path and check_file_exists(args.file_path):
        pipeline_data = parse_yaml(args.file_path)
    # If not, check if a dry-run command is provided
    elif args.dry_run_command:
        pipeline_data = load_yaml_from_dry_run(args.dry_run_command)
    else:
        print("No valid input provided. Either a file path or a dry-run command must be specified.")
        return
    # Debug statements to ensure 'jobs' and 'stages' are present in the data
    if 'jobs' not in pipeline_data:
        print(f"Debug: 'jobs' not found in pipeline_data: {pipeline_data}")
    if 'stages' not in pipeline_data:
        print(f"Debug: 'stages' not found in pipeline_data: {pipeline_data}")

    # Define the output path for the diagram
    output_path = 'output/pipeline_diagram'
    for ext in ['.dot', '.png']:
        if os.path.exists(output_path + ext):
            os.remove(output_path + ext)

    # Generate the DOT diagram from the pipeline data
    dot_diagram = generate_dot_diagram(pipeline_data)
    print(dot_diagram.source) # Print the DOT source code
    # Render the diagram to a PNG file and open it for viewing
    dot_diagram.render('output/pipeline_diagram', format='png', view=True)


if __name__ == "__main__":
    main()
