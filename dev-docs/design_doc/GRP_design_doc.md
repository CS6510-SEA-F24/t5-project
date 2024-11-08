# Graphical Representation of Pipelines (GRP)Design Document

## Overview
The Graphical Representation of Pipelines (GRP) project aims to create a visual representation of CI/CD pipeline configuration files. This feature is designed to enhance the understanding of pipeline structures and job dependencies, similar to the graphical representation provided by GitLab.

## Objectives
- To develop a tool that can convert YAML pipeline configuration files into a graphical format.
- To ensure that the graphical representation accurately reflects the stages, jobs, and their dependencies.
- To provide a user-friendly interface for visualizing complex pipeline structures.

## Scope
### Included
- Development of a graphical representation tool that processes YAML files.
- Visualization of stages, jobs, dependencies, and artifacts.
- Support for dynamic updates based on changes in the YAML configuration.

### Excluded
- Integration with external CI/CD systems beyond the YAML input.
- Advanced interactive features beyond basic visualization.

## Requirements
### Functional Requirements
1. The tool must accept a valid YAML file as input.
2. The graphical output must display stages and jobs according to the YAML configuration.
3. Job dependencies must be represented as arrows connecting the relevant job graphics.
4. Artifacts must be displayed in a separate graphical object, showing filesystem paths and regular expressions.

### Non-Functional Requirements
1. The tool should be user-friendly and intuitive.
2. The graphical representation must be responsive and visually appealing.
3. The system should handle errors gracefully, providing meaningful feedback to users.

## Architecture
The system architecture consists of the following components:
- **Input Module**: Responsible for reading and validating the YAML configuration file.
- **Processing Module**: Parses the YAML data and prepares it for visualization.
- **Rendering Module**: Generates the graphical representation using HTML, CSS, JavaScript, and SVG.
- **Output Module**: Exports the graphical representation in the desired format.

## System Architecture Diagram

## Technologies
- **Python**: As the primary programming language for backend processing.
- **Jinja2**: For rendering dynamic HTML content.
- **JavaScript**: To handle dynamic behaviors and interactions.
- **SVG**: For scalable vector graphics representation.
- **HTML/CSS**: For structuring and styling the web application.
- **PyYAML**: For parsing YAML configuration files.
- **Poetry**: For dependency management and project building.
- **Nox**: For automated builds, tests, and code checks.
- **GitHub Actions**: For CI/CD automation.


## Code Structure
```
├── main
│   ├── src
│   └── t5_grp
│       ├── assets
│       │   ├── main.css
│       │   └── main.js
│       ├── main.py
│       ├── parser
│       │   └── yaml_parser.py
│       ├── templates
│       │   └── pipeline_template.html
│       └── visualization
│           └── diagram_generator.py
└── tests
├── parser
│   └── test_yaml_parser.py
├── test_files
│   ├── invalid.yaml
│   └── valid.yaml
├── test_main.py
└── visualization
└── test_diagram_generator.py
```

Reference Information
Gitlab:https://docs.gitlab.com/ee/ci/pipelines/
