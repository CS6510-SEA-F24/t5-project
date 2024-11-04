# t5_grp

A tool to generate and visualize pipeline diagrams.


## Table of Contents
- [Features (WIP)]
- [Development Setup]
- - [Prerequisites]
- - [Build Instructions]
- [User Manual]
- [Pull Request Process]
- - [Creating a PR]
- - [Rules for PRs]
- [CI/CD Workflows]
- [License]

## Features (WIP)

## Development Setup

### Prerequisites

To use this project, you need:

- Python 3.12 or higher
- Poetry (for dependency management)

### Build Instructions

Clone the repository:
```bash
git clone https://github.com/CS6510-SEA-F24/t5-project.git
```
Build the Project:
Using Nox for Automated Builds, Tests, and Linting, file in `noxfile.py`:

We use nox to run automated sessions like testing, linting, and building the project.
Nox allows us to define a "do-all" type script to ensure everything runs in one command.

To run all sessions:

```bash
nox -s all
```

Install the dependencies using Poetry:

```bash
poetry install
```

Build the Project: Build source distribution and wheel files:

```bash
poetry build
```

```bash
poetry run 
# e.g. poetry run python -m t5_grp.main ./test.yaml
```
Running different files
```bash
poetry run python -m t5_grp.main <your_yaml_file_path>
```

```bash
poetry run black src/ tests
```

Lint Code (Flake8): Check code style against PEP8 guidelines:

```bash
poetry run flake8 src/ tests/
```

## User Manual
navigating to the project directory and running the script


## Pull Request Process

### Creating a PR

#### Always use feature branch to make change:

```bash
git checkout -b <branch_name> # create a new branch with <branch_name>
```

> Direct push to the `main` branch is strictly forbidden as this is the Production branch. All change
> should be merged with an approved PR.

#### Ensure your code is up-to-date with the `main` branch:

```bash
git config pull.rebase true # always use rebase to reconcile divergent branches
git pull
```

> Regularly pull from the `main` branch avoids conflicts pilling up.
> Please make sure you pull again before creating a PR.
#### Follow the PR Template:

- Your PR description should address any relevant context to help the reviewer to understand the
  PR. If this is related to an issue, reference the issue in the description.
- Make sure to use the checklist, and give explanations to any unchecked ones.

#### Check PR details:

- Make sure the origin and destination of the PR is correct, as well as everything in the Commits
  and Files changed tabs before clicking "Create Pull Request".

### Rules for PRs

#### PR Size Limit:

- PRs should not exceed 150 lines unless absolutely necessary.

  > To override this, add an `override-size-limit` label in the PR, and provide explanation in the
  > PR description.

#### Testing:

- Ensure all new code is properly tested.
#### Commit Guidelines:

- Use [meaningful commit messages](https://www.freecodecamp.org/news/how-to-write-better-git-commit-messages/).
  Squash commits if necessary to clean up the history.

#### Merging:

- When merging PRs, always use **SQUASH AND MERGE** to combine all changes into a single commit.

#### Review Timebox:

- Please post reviews within 24 hours after you received the review request, or ask for others to
  do the review.
## CI/CD Workflows

This project uses **GitHub Actions** for CI/CD automation. The configured CI/CD workflows are:

- **PR Size Check**:

    - This workflow is triggered when a new PR is created, or when a new commit is pushed to an existing PR.
    - It fails if the size of PR is greater than 150 lines, and no override label is provided.


- **Pipeline Run**:
    - This workflow is triggered when:
        - A PR is created/ updated.
        - A PR is merged.
    - This workflow will execute:
        - Build: Ensures the code builds successfully.
        - Run Unit Tests: All tests must pass.
        - Test Coverage Verification: Verifies that test coverage meets minimum requirements.
        - Code Quality Checks: Checkstyle and SpotBugs
        - Artifacts Upload: Build artifacts and generated reports are uploaded after pipeline run

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.