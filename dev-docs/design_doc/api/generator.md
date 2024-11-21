# Diagram Generator API

## Overview
The Diagram Generator module converts pipeline configurations into HTML visualizations.

## Input
Pipeline configuration object (as defined in parser output)

## Output
HTML visualization containing:
- Pipeline stages
- Jobs within stages
- Dependency arrows
- Artifact information

## Errors
- Template rendering errors
- Asset file errors (missing CSS/JS)
- Invalid job dependencies