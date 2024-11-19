"""
Pipeline Diagram Generator
=========================

This module provides functionality to generate visual diagrams for CI/CD pipelines.
    It converts pipeline configuration data into an HTML visualization with interactive
    elements and dependency arrows.

Key Features:
- HTML generation from pipeline configuration
- Asset management and copying
- Job dependency sorting and visualization
- Artifact tracking across stages

Main Components:
1. HTML Generation: Creates the visualization from templates
2. Data Extraction: Processes pipeline configuration
3. Job Management: Handles job dependencies and positioning
4. Asset Handling: Manages CSS, JS, and other static files
"""

import shutil
from jinja2 import Environment, FileSystemLoader
from typing import Any
import os
from ..config import (
    ASSET_FILES,
    ASSET_DIR_NAME,
    TEMPLATE_DIR_NAME,
    TEMPLATE_FILE,
    ASSETS_FOLDER,
)


def generate_html(data: dict[str, Any], output_path: str) -> None:
    """
    Generate HTML visualization of pipeline configuration.

    Args:
        data: Pipeline configuration containing stages, jobs, and dependencies
        output_path: Target path for the generated HTML file

    Raises:
        ValueError: If output_path is not provided

    The function performs the following steps:
    1. Extracts pipeline data from configuration
    2. Sets up Jinja2 templating environment
    3. Copies required assets (CSS/JS) to output directory
    4. Renders HTML template with pipeline data
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
    assets_dst_dir = os.path.join(output_dir, ASSETS_FOLDER)
    os.makedirs(assets_dst_dir, exist_ok=True)

    # Copy CSS and JS files
    for asset in ASSET_FILES:
        src = os.path.join(assets_src_dir, asset)
        dst = os.path.join(assets_dst_dir, asset)
        if os.path.exists(src):
            shutil.copy2(src, dst)

    html_output = template.render(pipeline=pipeline_data, asset_path=ASSETS_FOLDER)

    # Write the HTML content to the specified output path
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html_output)

    print(f"Generated output.html successfully at: {output_path}")


def sort_jobs_by_dependency(jobs: list) -> list:
    """Sort jobs based on dependency count and position"""
    return sorted(
        jobs, key=lambda x: (-x[1].get("dependency_count", 0), x[1].get("position", 0))
    )


def extract_pipeline_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    Extract and structure pipeline data for visualization.

    Args:
        data: Raw pipeline configuration dictionary

    Returns:
        Processed pipeline data with:
        - Organized stages and jobs
        - Calculated dependencies
        - Collected artifacts
        - Job positioning information

    The function processes:
    1. Pipeline stages and their order
    2. Job information and dependencies
    3. Artifact collection per stage
    4. Job positioning within stages
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

    for stage in pipeline_info["stages"]:
        stage_jobs = [
            (name, job)
            for name, job in pipeline_info["jobs"].items()
            if job["stage"] == stage["name"]
        ]
        stage["jobs"] = sort_jobs_by_dependency(stage_jobs)

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
    Process and add job information to pipeline structure.

    Args:
        pip_info: Pipeline information dictionary to update
        job: Job configuration dictionary
        job_name: Name of the job being processed
        stage_name: Name of the stage containing the job
        stage_artifacts: Dictionary tracking artifacts per stage
        all_artifacts: Set of all artifacts in pipeline

    The function handles:
    1. Job dependency counting and priority calculation
    2. Position management within stages
    3. Artifact collection and organization
    4. Dependency relationship recording

    Priority levels:
    0: No dependencies, not depended on
    1: No dependencies, is depended on
    2: Has dependencies, is depended on
    3: Has dependencies, not depended on
    """
    # Initialize jobs dictionary if it doesn't exist
    if "jobs" not in pip_info:
        pip_info["jobs"] = {}
    # Calculate how many other jobs depend on this job
    being_depended_count = sum(
        1
        for other_job in pip_info["jobs"].values()
        if job_name in other_job.get("needs", [])
    )
    # Count how many jobs this job depends on
    depending_count = len(job.get("needs", []))

    if depending_count == 0:
        priority = 1 if being_depended_count > 0 else 0
    else:
        priority = 2 if being_depended_count > 0 else 3
    # Create job entry with all necessary information
    pip_info["jobs"][job_name] = {
        "stage": stage_name,
        "needs": job.get("needs", []),
        "allow_failure": job.get("allow_failure", False),
        "id": f"job_{job_name}",
        "position": len(pip_info["jobs"]),
        "artifacts": job.get("artifacts", {}).get("paths", []),
        "dependency_count": priority,
    }
    # Process each dependency of the current job
    for need in job.get("needs", []):
        if need in pip_info["jobs"]:
            dep_job = pip_info["jobs"][need]
            # Adjust positions to maintain dependency order
            if dep_job["position"] > pip_info["jobs"][job_name]["position"]:
                temp_pos = dep_job["position"]
                dep_job["position"] = pip_info["jobs"][job_name]["position"]
                pip_info["jobs"][job_name]["position"] = temp_pos
            # Update dependency job's priority
            dep_depending_count = len(dep_job.get("needs", []))
            if dep_depending_count == 0:
                dep_job["dependency_count"] = 1
            else:
                dep_job["dependency_count"] = 2
        # Record dependency relationship
        pip_info["dependencies"].append(
            {
                "from": f"job_{need}",
                "to": f"job_{job_name}",
                "fromStage": pip_info["jobs"].get(need, {}).get("stage", ""),
                "toStage": stage_name,
            }
        )
    # Process job artifacts if they exist
    if "artifacts" in job:
        artifacts = job["artifacts"].get("paths", [])
        # Initialize stage artifacts set if needed
        if stage_name not in stage_artifacts:
            stage_artifacts[stage_name] = set()
        # Update stage and global artifact collections
        stage_artifacts[stage_name].update(artifacts)
        all_artifacts.update(artifacts)

        # update stage artifacts
        for stage in pip_info["stages"]:
            if stage["name"] == stage_name:
                stage["artifacts"].extend(artifacts)
                break
