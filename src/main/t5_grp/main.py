import argparse
from parser.yaml_parser import parse_yaml
from visualization.iagram_generator import generate_dot_diagram
from utils.helpers import check_file_exists


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
    args = parser.parse_args()
    file_path = args.file_path
    if not check_file_exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    pipeline_data = parse_yaml(file_path)
    dot_diagram = generate_dot_diagram(pipeline_data)
    print(dot_diagram.source)
    dot_diagram.render('output/pipeline_diagram', format='png', view=True)


if __name__ == "__main__":
    main()
