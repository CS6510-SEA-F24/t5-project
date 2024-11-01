import argparse
from parser.yaml_parser import parse_yaml
from visualization.iagram_generator import generate_dot_diagram
from utils.helpers import check_file_exists


def main():
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
