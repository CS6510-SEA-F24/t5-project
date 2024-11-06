import os
import subprocess
from io import StringIO
import yaml

"""
    Parse the YAML file at the given path and return the corresponding data structure.

    Parameters:
        file_path (str): The path to the YAML file to be parsed.

    Returns:
        dict | list: The parsed YAML content, typically as a dictionary or list.

    Raises:
        FileNotFoundError: If the file path is incorrect or the file does not exist.
        yaml.YAMLError: If the file content is not a valid YAML format.
"""
def parse_yaml(file_path):
    # Open and read the YAML file
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file) # Parse YAML content
        validate_yaml_keys(data) # Validate YAML keys
        return data # Return parsed data

"""
    Run the given command with `--dry-run` and parse its output as YAML.

    Parameters:
        command (str): The command to run with `--dry-run`.

    Returns:
        dict | list: The parsed YAML content, typically as a dictionary or list.

    Raises:
        RuntimeError: If the command fails.
        yaml.YAMLError: If the command output is not a valid YAML format.
"""
def load_yaml_from_dry_run(command):
    # Execute the command and capture its output
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    # Check if the command execution was successful
    if result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}: {result.stderr}")

    output = result.stdout # Get the command output
    data = yaml.safe_load(StringIO(output)) # Parse command output as YAML data
    validate_yaml_keys(data)   # Validate YAML keys
    return data  # Return parsed data

"""
    Validate the YAML structure to ensure it contains the required keys and correct data types.
    
    Parameters:
        yaml_data (dict | list): The parsed YAML content to validate.

    Raises:
        KeyError: If some required key is missing.
        TypeError: If the value type of some required key is incorrect.
"""
def validate_yaml_keys(yaml_data):
    # Define the required keys and their value types，will update if new requirements
    REQUIRED_KEYS = {
        'pipeline': dict,
        'stages': list,
        'jobs': list,
    }
    """
        Validate a job to ensure it contains the required keys 'name' and 'stage'.
        
        Parameters:
            job (dict): The job entry to validate.

        Raises:
            KeyError: If some required job key is missing.
    """
    def validate_job(job):
        required_job_keys = ['name', 'stage']
        for key in required_job_keys:
            if key not in job:
                raise KeyError(f"Job missing required key: {key}")
    # Validate top-level required keys and their value types
    for key, value_type in REQUIRED_KEYS.items():
        if key not in yaml_data:
            raise KeyError(f"Missing required key: {key}")
        if not isinstance(yaml_data[key], value_type):
            raise TypeError(f"Key '{key}' should be of type {value_type.__name__}")

    # # Validate each job in the jobs list
    for job in yaml_data.get('jobs', []):
        validate_job(job)


"""
    Check if a file exists at the given path.

    Parameters:
        file_path (str): The path to the file to be checked.

    Returns:
        bool: True if the file exists, False otherwise.
"""


def check_file_exists(file_path):
    return os.path.isfile(file_path)
