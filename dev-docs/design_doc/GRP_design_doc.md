# Graphical Representation of Pipelines (GRP) Design Document

## Table of Contents
1. [Overview](#overview)
    - Purpose
    - Problem Statement
    - Target Users
2. [Requirements](#requirements)
    - Functional Requirements
    - Non-Functional Requirements
3. [Objectives](#objectives)
4. [Scope](#scope)
5. [Pipeline Schema](#pipeline-schema)
    - Data Model
    - YAML Structure
    - Validation Rules
6. [Architecture](#architecture)
    - System Overview
    - Component Design
    - Data Flow
    - Module Interactions
7. [Technologies](#technologies)
    - Core Stack
    - Development Tools
8. [Implementation](#implementation)
    - Project Structure
    - Command Interface
    - Key Components
9. [References](#references)

## Overview

### Purpose
The GRP tool visualizes CI/CD pipeline configurations through an intuitive graphical interface, transforming YAML-based pipeline definitions into interactive visual representations.

### Problem Statement
CI/CD pipelines defined in YAML format can become complex and difficult to understand, especially for:
- Large projects with multiple stages
- Pipelines with complex dependencies
- Teams needing to understand pipeline flow
- New team members learning the pipeline structure

### Target Users
- DevOps Engineers
- Software Developers
- CI/CD Pipeline Maintainers
- Project Managers

## Requirements

### Functional Requirements
1. **YAML Processing**
    - Parse and validate YAML pipeline configurations
    - Support standard CI/CD pipeline structures
    - Handle job dependencies and artifacts

2. **Visualization**
    - Generate interactive HTML output
    - Display pipeline stages and jobs
    - Show dependencies as arrows
    - Represent artifacts and their paths

3. **Customization**
    - Support multiple themes (light/dark)
    - Allow stage gap adjustments
    - Provide cleanup options

### Non-Functional Requirements
1. **Performance**
    - Quick YAML parsing
    - Efficient HTML generation
    - Responsive visualization

2. **Usability**
    - Clear command-line interface
    - Intuitive visualization layout
    - Helpful error messages

3. **Maintainability**
    - Modular code structure
    - Comprehensive test coverage
    - Clear documentation

## Objectives
1. Create a tool that converts YAML pipeline configurations into visual representations
2. Provide clear visualization of pipeline structure and dependencies
3. Support standard CI/CD pipeline features
4. Ensure ease of use through command-line interface

## Scope

### Included
- YAML pipeline configuration parsing
- Interactive HTML visualization generation
- Stage and job dependency visualization
- Artifact representation
- Theme customization
- Command-line interface

### Excluded
- Real-time pipeline execution monitoring
- Integration with specific CI/CD platforms
- Pipeline editing capabilities
- Advanced animation effects

## Pipeline Schema

### YAML Structure
```yaml
pipeline:
  name: string (required)
  stages:
    - stage1
    - stage2
  jobs:
    - name: string
      stage: string
      script:
        - command1
        - command2
      dependencies:
        - job1
      artifacts:
        paths:
          - path1
      allow_failure: boolean
```

### Validation Rules
1. Pipeline name must be present
2. At least one stage required
3. Each job must reference valid stage
4. Dependencies must reference existing jobs,dependencies is optional
5. Artifact paths must be valid strings,artifact is optional

## Architecture

### System Overview
![System Architecture](./grp-system-architecture.png "GRP System Architecture")

### Component Design
1. **Input Module**
    - YAML file reading
    - Schema validation
    - Error handling

2. **Processing Module**
    - Pipeline data structure creation
    - Dependency resolution
    - Artifact tracking

3. **Visualization Module**
    - HTML template rendering
    - CSS styling
    - JavaScript interactivity

### Data Flow
1. Read YAML file → Validate structure → Create pipeline object
2. Process dependencies → Generate layout → Create visualization
3. Apply styling → Add interactivity → Output HTML

### Module Interactions
- Parser → Pipeline Object → Visualization Generator
- Template Engine ← Assets ← Visualization Generator
- Error Handler ← All Modules

## Technologies

### Core Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.12 | Core processing |
| PyYAML | 6.0.2 | YAML parsing |
| Jinja2 | 3.1.4 | HTML templating |

### Development Tools
| Tool | Version | Purpose |
|------|---------|---------|
| Poetry | latest | Dependency management |
| pytest | 7.4.4 | Testing |
| black | 24.10.0 | Code formatting |
| flake8 | 6.0.0 | Linting |

## Implementation

### Project Structure
```
src/
├── main/
│   └── t5_grp/
│       ├── assets/
│       ├── parser/
│       ├── templates/
│       └── visualization/
└── tests/
    ├── parser/
    ├── test_files/
    └── visualization/
```

### Command Interface
```bash
Usage: cicd [-h] [-o OUTPUT] [-t {light,dark}] [--stage-gap STAGE_GAP] [--cleanup] YAML_FILE_PATH

Arguments:
  YAML_FILE_PATH                     Full path to your YAML configuration file (required, must exist)

Options:
  -h, --help                        Show this help message and exit
  -o OUTPUT, --output OUTPUT        Output file path (default: output.html)
  -t {light,dark}, --theme {light,dark}
                                   Select visualization theme (default: light)
  --stage-gap STAGE_GAP            Gap between stages in pixels (default: 60)
  --cleanup                        Delete generated files after creation
```

### Key Components
1. **Parser Module**
    - YAML file parsing
    - Schema validation
    - Error handling

2. **Visualization Module**
    - HTML generation
    - CSS styling
    - JavaScript functionality

3. **Template System**
    - Layout templates
    - Theme support
    - Component rendering

## References

### Documentation
- [GitLab CI/CD Pipeline Documentation](https://docs.gitlab.com/ee/ci/pipelines/)
- [YAML Specification](https://yaml.org/spec/1.2.2/)

### Related Projects
- [GitLab Pipeline Visualizer](https://gitlab.com/gitlab-org/gitlab/-/tree/master/app/assets/javascripts/pipelines)