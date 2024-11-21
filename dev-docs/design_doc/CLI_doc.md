# CLI Documentation

## Commands
poetry run cicd <yaml_file_path> [options]

## Options
Required:
- yaml_file_path      Path to CI/CD config YAML file

Optional:
- --output, -o       Output HTML file path (default: output.html)
- --theme, -t        Visual theme (light/dark) (default: light)
- --stage-gap        Gap between stages in pixels (default: 60)
- --help, -h         Show this help message

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
