# Graphical Representation of Pipelines (GRP)Design Document
## Table of Contents
1. [Overview](#overview)
2. [Objectives](#objectives)
3. [Scope](#scope)
4. [Requirements](#requirements)
5. [Architecture](#architecture)
6. [Technologies](#technologies)
7. [Pipeline Schema](#pipeline-schema)
8. [Project Structure](#structure)
9. [References](#references)
## Overview

### Purpose
The GRP tool visualizes CI/CD pipeline configurations through an intuitive graphical interface. It helps developers and DevOps teams better understand and manage their pipeline structures.

### Problem Statement
Complex CI/CD pipelines can be difficult to understand when represented only in YAML format. This tool bridges the gap between textual configuration and visual comprehension.

### Key Features
1. YAML to visual pipeline conversion
2. Interactive stage and job visualization
3. Dependency tracking and artifact management
4. Customizable visual themes

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

### System Architecture Diagram

![System Architecture](./grp-system-architecture.png "GRP System Architecture")

## Technologies

### Core Stack
| Technology | Version | Purpose | Key Benefits |
|------------|---------|---------|--------------|
| Python | 3.12 | Backend Processing | - Rich ecosystem<br>- Cross-platform<br>- CI/CD tooling |
| PyYAML | 6.0.2 | YAML Processing | - Industry standard<br>- Robust parsing |
| Jinja2 | 3.1.4 | Template Engine | - Web integration<br>- Powerful features |

### Development Tools
| Tool | Version | Purpose |
|------|---------|---------|
| Poetry | latest | Package management |
| pytest | 7.4.4 | Testing framework |
| black | 24.10.0 | Code formatting |
| flake8 | 6.0.0 | Code linting |

## Pipeline Schema

### Root Elements
- pipeline (required)
    - name: string (required)
    - stages: string[] (required)
    - jobs: Job[] (required)

### Job Object
- name: string (required)
- stage: string (required, must match a stage name)
- script: string[] (optional)
- needs: string[] (optional)
- artifacts:
    - paths: string[] (optional)
- allow_failure: boolean (optional)

## Example
- [test.yaml](/Users/yoyowu/NEU/t5_grp/src/tests/test_files/test.yaml)

## Structure
### Code Structure
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

### Component Description

#### Main Components
1. **Parser Module**
    - Handles YAML file parsing and validation
    - Converts YAML to internal data structure

2. **Visualization Module**
    - Generates HTML/SVG visualization
    - Manages job dependencies and artifacts
    - Handles asset management

3. **Templates**
    - Contains Jinja2 templates for HTML generation
    - Defines visualization layout and structure

4. **Assets**
    - CSS for styling
    - JavaScript for interactivity
    - Static resources

#### Test Structure
- Unit tests for each module
- Test files for validation
- Integration tests for full pipeline


### Command Syntax
- `yaml_file_path`    Path to CI/CD configuration YAML file
```bash
poetry run cicd <yaml_file_path> [options]
```
#### Optional
- `-o, --output`      Output HTML file path (default: output.html)
- `-t, --theme`       Visual theme (light/dark) (default: light)
- `--stage-gap`       Gap between stages in pixels (default: 60)
- `--cleanup`         Delete generated files after creation
- `-h, --help`        Show help message

## References

### Documentation
- [GitLab CI/CD Pipeline Documentation](https://docs.gitlab.com/ee/ci/pipelines/)
- [YAML Specification](https://yaml.org/spec/1.2.2/)

### Related Projects
- [GitLab Pipeline Visualizer](https://gitlab.com/gitlab-org/gitlab/-/tree/master/app/assets/javascripts/pipelines)

