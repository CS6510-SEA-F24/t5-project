# CLI Documentation
## Overview
The CLI tool generates HTML visualizations from CI/CD pipeline YAML configurations.

## Command Syntax
```bash
poetry run cicd <yaml_file_path> [options]
```
## Options
### Required
- `yaml_file_path`    Path to CI/CD configuration YAML file

### Optional
- `-o, --output`      Output HTML file path (default: output.html)
- `-t, --theme`       Visual theme (light/dark) (default: light)
- `--stage-gap`       Gap between stages in pixels (default: 60)
- `--cleanup`         Delete generated files after creation
- `-h, --help`        Show help message

## Examples

Examples:
### Basic usage
```bash
 poetry run cicd /Users/yoyowu/NEU/t5_grp/src/tests/test_files/test.yaml 
```
 Generated output.html successfully at: /Users/yoyowu/NEU/t5_grp/output.html

### With custom output path
```bash
 poetry run cicd /Users/yoyowu/NEU/t5_grp/src/tests/test_files/test.yaml -o fullstack_pipeline.html 
```

 Generated output.html successfully at: /Users/yoyowu/NEU/t5_grp/fullstack_pipeline.html

### With dark theme
```bash
 poetry run cicd /Users/yoyowu/NEU/t5_grp/src/tests/test_files/test.yaml -t dark
```
### With custom stage gap
```bash
 poetry run cicd /Users/yoyowu/NEU/t5_grp/src/tests/test_files/test.yaml --stage-gap 100
```
### Generate and Clean Up
```bash
poetry run cicd /Users/yoyowu/NEU/t5_grp/src/tests/test_files/test.yaml --cleanup
```
Cleaned up generated files.
### Combined Options

Custom output with dark theme
```bash
 poetry run cicd /Users/yoyowu/NEU/t5_grp/src/tests/test_files/test.yaml -t dark
```
Custom output with stage gap and dark theme
 -
```bash
 poetry run cicd /Users/yoyowu/NEU/t5_grp/src/tests/test_files/test.yaml -o ws.html -t dark --stage-gap 9
```
Generated output.html successfully at: /Users/yoyowu/NEU/t5_grp/ws.html


## Generated Files
The tool creates the following files:
1. Main HTML visualization file (specified by --output)
2. YAML content viewer HTML file (*_yaml.html)
3. Assets directory with required resources

When using --cleanup, all generated files are automatically removed after creation.