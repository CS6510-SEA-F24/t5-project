from jinja2 import Environment, FileSystemLoader
from typing import Any
import os
import shutil
"""
This module provides functions to generate an HTML representation for a pipeline diagram, using Jinja2 template rendering.

Functions:
    generate_html(data: dict) -> None:
        Generates an HTML file from the provided pipeline data.
        
    extract_pipeline_data(data: dict) -> dict:
        Processes and extracts relevant pipeline data from input and organizes it into a structured format.

Usage:
    Use `generate_html(data)` to generate an HTML file representing the pipeline.
    The module relies on Jinja2 templates to structure the HTML output.
"""

def generate_html(data: dict) -> None:
    """
    Generates an HTML file from the given pipeline data.

    Args:
        data (dict): The input data containing pipeline structure, stages, jobs, and artifacts.

    This function sets up the Jinja2 Environment, loads the pipeline template, and renders the HTML output.
    The resulting HTML file is saved in the 'tests' directory.
    """
    # Extract pipeline data
    pipeline_data = extract_pipeline_data(data)
    # current_dir = os.path.dirname(__file__)
    # #debug
    # shutil.copy2(os.path.join(current_dir, '..', 'assets', 'main.css'), os.path.join(current_dir, '..', '..', 'main.css'))
    # shutil.copy2(os.path.join(current_dir, '..', 'assets', 'main.js'), os.path.join(current_dir, '..', '..', 'main.js'))

    # Setting up the Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'templates')),
        autoescape=True  # Enable auto-escaping
    )
    # Loading the template
    template = env.get_template('pipeline_template.html')
    # Rendering the template with the pipeline data
    html_output = template.render(pipeline=pipeline_data)

    # Ensure the output directory exists
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src', 'main'))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Defining the output path
    output_path = os.path.join(output_dir, 'output.html')
    # Writing the rendered HTML to a file
    with open(output_path, 'w') as file:
        file.write(html_output)
    print("Generated output.html successfully.")


def extract_pipeline_data(data: dict) -> dict:
    """
    Extracts and processes pipeline data from the given input.

    Args:
        data (dict): The input data containing pipeline structure, stages, jobs, and artifacts.

    Returns:
        dict: A dictionary containing processed pipeline data sorted into stages, jobs, and artifacts.

    This function processes job dependencies, stages, and artifacts and prepares a structured data format for
    rendering in the HTML template.
    """
    pipeline_info: dict[str, Any] = {
        'name': data.get('pipeline', {}).get('name', 'Unnamed Pipeline'),
        'stages': data.get('stages', []),
        'jobs': {},
        'artifacts': {},
        'dependencies': []
    }

    # Collections for artifact information
    all_artifacts: set[str] = set()
    stage_artifacts: dict[str, set[str]] = {}

    # Process jobs and their artifacts
    for job in data.get('jobs', []):
        job_name = job.get('name')
        stage_name = job.get('stage')

        if job_name:
            # Add job information to pipeline data
            pipeline_info['jobs'][job_name] = {
                'stage': stage_name,
                'needs': job.get('needs', []),
                'allow_failure': job.get('allow_failure', False),
                'id': f'job_{job_name}',  # Unique ID for job to facilitate arrow drawing
                'position': len(pipeline_info['jobs']),# Position for arrow layout
                'artifacts': job.get('artifacts', {}).get('paths', [])  # Ensure artifacts field is populated
            }
            if not stage_name:
                raise ValueError(f"Stage is required for job: {job_name}")

            # Process and collect artifacts for each stage
            for need in job.get('needs', []):
                pipeline_info['dependencies'].append({
                    'from': f'job_{need}',
                    'to': f'job_{job_name}',
                    'fromStage': pipeline_info['jobs'].get(need, {}).get('stage', ''),
                    'toStage': stage_name
                })

            # Process and collect artifacts for each stage
            if 'artifacts' in job:
                artifacts = job['artifacts'].get('paths', [])
                if stage_name not in stage_artifacts:
                    stage_artifacts[stage_name] = set()
                stage_artifacts[stage_name].update(artifacts)
                all_artifacts.update(artifacts)

    # Adding artifacts information to each stage
    for stage, artifacts in stage_artifacts.items():
        pipeline_info['artifacts'][stage] = sorted(list(artifacts))

    # Add a summary of all artifacts in the pipeline
    pipeline_info['all_artifacts'] = sorted(list(all_artifacts))


    return pipeline_info