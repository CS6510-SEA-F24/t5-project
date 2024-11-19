import shutil

from jinja2 import Environment, FileSystemLoader
from typing import Any
import os
from ..config import (
    ASSET_FILES,
    ASSET_DIR_NAME,
    TEMPLATE_DIR_NAME,
    TEMPLATE_FILE,
    PROJECT_ROOT,
    ASSETS_FOLDER,
    SUCCESS_MESSAGE,
)

"""
This module provides functionality to generate visual diagrams for CI/CD
pipelines.
"""


def generate_html(data: dict[str, Any], output_path: str) -> None:
    """Generate HTML visualization of pipeline

    Args:
        data: Pipeline configuration data
        output_path: Path where HTML file should be generated

    Raises:
        ValueError: If output_path is not provided
    """
    if not output_path:
        raise ValueError("output_path must be provided")
    # Extract pipeline data
    pipeline_data = extract_pipeline_data(data)

    # Setting up the Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "..", TEMPLATE_DIR_NAME)
        ),
        autoescape=True,
    )

    # Loading the template
    template = env.get_template(TEMPLATE_FILE)

    # Rendering the template with the pipeline data
    html_output = template.render(pipeline=pipeline_data, asset_path=ASSET_DIR_NAME)

    # Ensure the directory for output_path exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create assets directory and copy resources
    assets_src_dir = os.path.join(os.path.dirname(__file__), "..", ASSETS_FOLDER)
    assets_dst_dir = os.path.join(output_dir, PROJECT_ROOT, ASSETS_FOLDER)
    os.makedirs(assets_dst_dir, exist_ok=True)

    # Copy CSS and JS files
    for asset in ASSET_FILES:
        src = os.path.join(assets_src_dir, asset)
        dst = os.path.join(assets_dst_dir, asset)
        if os.path.exists(src):
            shutil.copy2(src, dst)

    # Write the HTML content to the specified output path
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html_output)

    print(SUCCESS_MESSAGE.format(output_path))


def extract_pipeline_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    Extract relevant data from the provided pipeline configuration.

    Args:
        data (dict): The pipeline configuration to extract data from.

    Returns:
        dict: Extracted relevant data from the configuration.
    """
    pipeline_info = {
        "name": data["pipeline"]["name"],
        "stages": [],
        "jobs": {},
        "dependencies": [],
        "artifacts": {},
        "all_artifacts": [],
    }

    stage_artifacts = {}
    all_artifacts = set()

    # Extract stages - stages is at root level in YAML
    stages = data.get("stages", [])
    for stage_name in stages:
        stage_info = {"name": stage_name, "artifacts": []}
        pipeline_info["stages"].append(stage_info)

    # Extract jobs - jobs is at root level and is a list in YAML
    jobs = data.get("jobs", [])
    for job in jobs:
        job_name = job.get("name")
        stage_name = job.get("stage")
        if job_name and stage_name:
            add_job_info(
                pipeline_info, job, job_name, stage_name, stage_artifacts, all_artifacts
            )

    # Adding artifacts information to each stage
    for stage, artifacts in stage_artifacts.items():
        pipeline_info["artifacts"][stage] = sorted(list(artifacts))

    # Add a summary of all artifacts in the pipeline
    pipeline_info["all_artifacts"] = sorted(list(all_artifacts))

    return pipeline_info


def add_job_info(
    pip_info: dict[str, Any],
    job: dict[str, Any],
    job_name: str,
    stage_name: str,
    stage_artifacts: dict[str, set[str]],
    all_artifacts: set[str],
) -> None:
    """
    Add job information to the pipeline info structure.

    Args:
        pip_info (dict): The pipeline info where the job data will be stored.
        job (dict): The job information.
        job_name (str): The name of the job.
        stage_name (str): The name of the stage to which this job belongs.
        stage_artifacts (dict): The dictionary to record stage artifacts.
        all_artifacts (set): The set to record all artifacts.

    Returns:
        None
    """
    being_depended_count = sum(
        1
        for other_job in pip_info["jobs"].values()
        if job_name in other_job.get("needs", [])
    )

    depending_count = len(job.get("needs", []))

    if depending_count == 0:
        priority = 1 if being_depended_count > 0 else 0
    else:
        priority = 2 if being_depended_count > 0 else 3

    pip_info["jobs"][job_name] = {
        "stage": stage_name,
        "needs": job.get("needs", []),
        "allow_failure": job.get("allow_failure", False),
        "id": f"job_{job_name}",
        "position": len(pip_info["jobs"]),
        "artifacts": job.get("artifacts", {}).get("paths", []),
        "dependency_count": priority,
    }

    for need in job.get("needs", []):
        if need in pip_info["jobs"]:
            dep_job = pip_info["jobs"][need]
            dep_depending_count = len(dep_job.get("needs", []))
            if dep_depending_count == 0:
                dep_job["dependency_count"] = 1
            else:
                dep_job["dependency_count"] = 2

        pip_info["dependencies"].append(
            {
                "from": f"job_{need}",
                "to": f"job_{job_name}",
                "fromStage": pip_info["jobs"].get(need, {}).get("stage", ""),
                "toStage": stage_name,
            }
        )

    if "artifacts" in job:
        artifacts = job["artifacts"].get("paths", [])
        if stage_name not in stage_artifacts:
            stage_artifacts[stage_name] = set()
        stage_artifacts[stage_name].update(artifacts)
        all_artifacts.update(artifacts)

        # update stage artifacts
        for stage in pip_info["stages"]:
            if stage["name"] == stage_name:
                stage["artifacts"].extend(artifacts)
                break
