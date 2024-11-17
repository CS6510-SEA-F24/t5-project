from jinja2 import Environment, FileSystemLoader
from typing import Any
import os

"""
This module provides functionality to generate visual diagrams for CI/CD
pipelines.
"""


def generate_html(data: dict[str, Any], output_dir: str) -> None:
    """
    Generates an HTML file visualizing the CI/CD pipeline stages and jobs.

    Args:
        data (dict): The validated YAML data representing pipeline
        stages and jobs.

    Returns:
        writes the generated HTML
        output to a file.
    """
    # Extract pipeline data
    pipeline_data = extract_pipeline_data(data)

    # Setting up the Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "..", "templates")
        ),
        autoescape=True,
    )

    # Loading the template
    template = env.get_template("pipeline_template.html")

    # Rendering the template with the pipeline data
    html_output = template.render(pipeline=pipeline_data)

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Defining the output path
    output_path = os.path.join(output_dir, "output.html")

    # Writing the rendered HTML to a file
    with open(output_path, "w") as file:
        file.write(html_output)

    print(f"Generated output.html successfullyat: {output_path}")


def extract_pipeline_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    Extracts and organizes pipeline data from the provided YAML data.

    Args:
        data (dict): The validated YAML data containing pipeline information.

    Returns:
        dict: A dictionary containing organized pipeline information, including
        stages, jobs, dependencies, and artifacts.
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
    for stage_name in data["stages"]:
        stage_info = {"name": stage_name, "artifacts": []}  # 初始化 artifacts 列表
        pipeline_info["stages"].append(stage_info)

    for job in data.get("jobs", []):
        job_name = job.get("name")
        stage_name = job.get("stage")

        if job_name:
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
    """Add job information to the pipeline data."""
    reverse_deps_count = sum(
        1
        for other_job in pip_info["jobs"].values()
        if job_name in other_job.get("needs", [])
    )

    pip_info["jobs"][job_name] = {
        "stage": stage_name,
        "needs": job.get("needs", []),
        "allow_failure": job.get("allow_failure", False),
        "id": f"job_{job_name}",
        "position": len(pip_info["jobs"]),
        "artifacts": job.get("artifacts", {}).get("paths", []),
        "dependency_count": len(job.get("needs", [])) + reverse_deps_count,
    }

    if not stage_name:
        raise ValueError(f"Stage is required for job: {job_name}")

    # Process dependencies
    for need in job.get("needs", []):
        pip_info["dependencies"].append(
            {
                "from": f"job_{need}",
                "to": f"job_{job_name}",
                "fromStage": pip_info["jobs"].get(need, {}).get("stage", ""),
                "toStage": stage_name,
            }
        )

    # Process and collect artifacts for each stage
    if "artifacts" in job:
        artifacts = job["artifacts"].get("paths", [])
        for stage in pip_info["stages"]:
            if stage["name"] == stage_name:
                stage["artifacts"].extend(artifacts)
                break
        if stage_name not in stage_artifacts:
            stage_artifacts[stage_name] = set()
        stage_artifacts[stage_name].update(artifacts)
        all_artifacts.update(artifacts)

        if stage_name not in pip_info["artifacts"]:
            pip_info["artifacts"][stage_name] = []
        pip_info["artifacts"][stage_name].extend(artifacts)
