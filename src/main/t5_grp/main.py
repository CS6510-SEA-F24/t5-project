import os
from t5_grp.visualization import diagram_generator
import argparse
from .parser import yaml_parser


def main(
    yaml_file_path,
    output_path="output.html",
    theme="light",
    stage_gap=60,
):
    """
    Parses the given YAML file and generates an HTML visualization.

    Args:
        yaml_file_path (str): Path to the YAML file containing the CI/CD configuration.
        output_path (str): Path where the visualization will be generated.
        theme (str): Visual theme to apply (light/dark).
        stage_gap (int): Gap between stages in pixels.
    """
    try:
        data = yaml_parser.parse_yaml(yaml_file_path)
        if data is None:
            print("Failed to parse YAML file or validation error occurred.")
            print(f" @{os.path.basename(yaml_file_path)} ")
            return

        data["__file__"] = yaml_file_path

        diagram_generator.generate_html(
            data,
            output_path=output_path,
            theme=theme,
            stage_gap=stage_gap,
        )
        print(f"Generated output.html successfully at: {os.path.abspath(output_path)}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def cli():
    parser = argparse.ArgumentParser()

    parser.add_argument("yaml_file", help="Path to CI/CD config YAML file")

    parser.add_argument(
        "-o",
        "--output",
        default="output.html",
        help="Output file path (default: output.html)",
    )

    parser.add_argument(
        "-t",
        "--theme",
        choices=["light", "dark"],
        default="light",
        help="Select visualization theme (light/dark)",
    )

    parser.add_argument(
        "--stage-gap",
        type=int,
        default=60,
        help="Gap between stages in pixels (default: 60)",
    )

    args = parser.parse_args()
    main(
        args.yaml_file,
        output_path=args.output,
        theme=args.theme,
        stage_gap=args.stage_gap,
    )


if __name__ == "__main__":
    cli()
