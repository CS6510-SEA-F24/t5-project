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
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
