# t5_grp

A tool for generating visual representations of CI/CD pipelines from YAML files. This tool helps you visualize your pipeline stages, jobs, dependencies, and artifacts in an interactive HTML format.

## Table of Contents
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Development Guide](#development-guide)
- [Pull Request Process](#pull-request-process)
- [License](#license)

## Installation

### Requirements
- Python 3.12 or higher
- pip (Python package installer)

### Install Methods

1. **Using pip (Recommended)**
```bash
pip install t5_grp
```

2. **From source**
```bash
git clone https://github.com/CS6510-SEA-F24/t5-project.git
cd t5-project
poetry install
```

## Quick Start

1. **Create a YAML file** (e.g., `pipeline.yaml`):
```yaml
pipeline:
  name: Simple Pipeline  # Pipeline name
  stages:               # Define stages
    - build
    - test
  jobs:                # Define jobs
    - name: compile
      stage: build     # Job belongs to build stage
      script:
        - echo "Building..."
```

2. **Generate visualization**:
```bash
cicd ./src/tests/test_files/pipeline.yaml
```

3. **View result**: Open `output.html` in your browser

## Usage Guide

### Command Options
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

### Examples
```bash
# Show help message
cicd --help

# Basic usage with relative path (file must exist)
cicd ./src/tests/test_files/pipeline.yaml

# Basic usage with absolute path
cicd /Users/username/project/pipeline.yaml

# Custom output file with dark theme
cicd /path/to/existing/pipeline.yaml -o my_pipeline.html -t dark

# Adjust stage gap between pipeline stages
cicd ./src/tests/test_files/pipeline.yaml --stage-gap 80

# Generate and then clean up all files (for testing)
cicd ./src/tests/test_files/pipeline.yaml --cleanup
```

### Generated Files
When running the tool, it creates:
1. Main output HTML file (default: `output.html`)
2. YAML HTML file (`{yaml_filename}_yaml.html`)

When using `--cleanup`:
- All generated files will be deleted after creation
- Useful for testing the generation process
- Note: Don't use cleanup if you want to keep the visualization

### YAML Configuration
```yaml
pipeline:
  name: Advanced Pipeline  # Pipeline name
  stages:                 # Define pipeline stages in order
    - build
    - test
    - deploy
  jobs:                  # Define jobs within stages
    - name: compile
      stage: build       # Job belongs to build stage
      script:           # Commands to execute
        - echo "Building..."
      artifacts:         # Define output artifacts
        paths:
          - dist/
      
    - name: unit-test
      stage: test        # Job belongs to test stage
      dependencies:      # Define job dependencies
        - compile       # This job runs after compile job
      script:
        - echo "Testing..."
```

### Features
- Multiple stages and jobs support
- Job dependencies visualization
- Artifact tracking
- Interactive HTML output
- Customizable themes and stage gaps
- Optional cleanup functionality

## Development Guide

### Prerequisites
- Python 3.12 or higher
- Poetry (for dependency management)

### Setup Development Environment

1. **Clone repository**
```bash
git clone https://github.com/CS6510-SEA-F24/t5-project.git
cd t5-project
```

2. **Install development dependencies**
```bash
poetry install
```

3. **Run tests**
```bash
# All tests
poetry run pytest

# With coverage
poetry run pytest --cov=src/ --cov-report=term-missing --cov-fail-under=60
```

4. **Code quality**
```bash
# Lint code
poetry run flake8 src

# Format code
poetry run black src

# Run all checks
poetry run nox -s all
```

## Pull Request Process

### Creating a PR

1. **Create feature branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make changes and test**
```bash
poetry run pytest
poetry run nox -s all
```

3. **Submit PR**
- Follow PR template
- Ensure tests pass
- Update documentation if needed

### Rules for PRs
- Keep changes focused and small
- Follow coding standards
- Include tests for new features
- Update documentation as needed

### Merging
- When merging PRs, always use **SQUASH AND MERGE** to combine all changes into a single commit

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.