import os
import yaml

"""
This module provides functionality for parsing and validating YAML files.
Functions:
    validate_yaml(data):
        Validates the structure of the YAML data to ensure required keys are
        present and correctly formatted.
    parse_yaml(file_path):
        Parses a given YAML file, validates its content, and returns the data
        if the file is valid.
Usage:
    Use `parse_yaml(file_path)` to read and validate a YAML file. If the file
    is valid, the parsed data is returned.
    If the file is invalid or does not exist, errors are printed to the
    console and None is returned.
"""


def validate_yaml(data):
    """
    Validates that the required keys are present in the YAML data.

    Args:
        data (dict): The parsed YAML data.

    Returns:
        dict: The original YAML data if valid.

    Raises:
        ValueError: If required keys are missing or each job does not have
        'name' and 'stage' keys.
    """
    required_keys = {"pipeline", "stages", "jobs"}

    # Check if the required keys are present in the data
    if not required_keys.issubset(data.keys()):
        missing_keys = required_keys - data.keys()
        raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")

    # Check each job for the presence of 'name' and 'stage' keys
    for job in data.get("jobs", []):
        if "name" not in job or "stage" not in job:
            raise ValueError("Each job must have 'name' and 'stage' keys.")


def get_node_line(node):
    """Get the line number of a YAML node"""
    if hasattr(node, "start_mark"):
        return node.start_mark.line + 1
    return 0


def parse_yaml(file_path):
    """
    Parses a YAML file, validates its content, and returns the data.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        dict: The validated YAML data if the file is valid.
        None: If the file does not exist or contains invalid data.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return None

    # Open and read the file, then parse its content
    with open(file_path, "r") as file:
        try:
            # First pass: Get the raw data with line numbers
            content = file.read()
            data = yaml.safe_load(content)
            lines = content.split("\n")
            job_lines = {}
            for i, line in enumerate(lines, 1):
                if "  - name:" in line:
                    job_name = line.split("name:")[1].strip()
                    job_lines[job_name] = i

            # Add line numbers to jobs
            if isinstance(data, dict) and "jobs" in data:
                for job in data["jobs"]:
                    if isinstance(job, dict) and "name" in job:
                        job["__line__"] = job_lines.get(job["name"], 0)

            validate_yaml(data)
            return data
        # Catch YAML specific errors
        except yaml.YAMLError as e:
            print(f"Error: Invalid YAML format. {e}")
            return None
        # Catch validation errors
        except ValueError as e:
            print(f"Validation Error: {e}")
            return None
