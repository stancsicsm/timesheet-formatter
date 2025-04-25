# Timesheet Formatter

This is a simple Python script to format the output of the Timesheet Tool to a Workfront compatible format.

## Installation
### Using uv (Recommended)
```bash
uv sync
```

### Using pip
It is recommended to use a virtual environment when installing it with this method.
```bash
python -m pip install .
```

## Usage
Before running the script, make sure you have a `.env` file in the root directory (set the variables based on `.env.example`).
You can create the required Jira API token [here](https://id.atlassian.com/manage-profile/security/api-tokens).

You can run the script using `uv run src/main.py` (or `python src/main.py`).
