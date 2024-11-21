# Pipeline YAML Schema

## Root Elements
- pipeline (required)
    - name: string (required)
    - stages: string[] (required)
    - jobs: Job[] (required)

## Job Object
- name: string (required)
- stage: string (required, must match a stage name)
- script: string[] (required)
- needs: string[] (optional)
- artifacts:
    - paths: string[] (optional)
- allow_failure: boolean (optional)

## Example
 - [test.yaml](/Users/yoyowu/NEU/t5_grp/src/tests/test_files/test.yaml)