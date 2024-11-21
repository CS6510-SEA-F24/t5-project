# YAML Parser API

## Overview
The YAML Parser module is responsible for reading and validating pipeline configuration files.

## Input
- YAML file path (string)
- Configuration must follow the schema defined in `src/tests/test_files/test.yaml` (lines 1-66)

## Output
Pipeline configuration object containing:
- Pipeline name
- Stages list
- Jobs configuration
- Dependencies
- Artifacts information

## Errors
- Invalid YAML syntax
- Missing required fields (pipeline, stages, jobs)
- Invalid stage/job configuration
- Invalid dependencies