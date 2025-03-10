# Deflakyzavr Plugin

This plugin creates a duty ticket in JIRA. It can be configured using command-line arguments or a configuration file (`setup.cfg`).

## Installation

To install the plugin, use pip:

```sh
pip install deflakyzavr
```

## Configuration
You can configure the plugin using a configuration file (setup.cfg). Below is an example of the configuration file:
```
[deflakyzavr]
jira_server = https://your-jira-server.com
jira_user = your_username
jira_password = your_password
jira_project = your_project_key
jira_components = component1,component2
epic_link_field = customfield_10011
jira_epic = EPIC-123
issue_type = 3
planned_field = customfield_10012
duty_label = flaky_duty
dry_run = false
```

## Usage
You can run the plugin using the following command:
```
python -m deflakyzavr --config path/to/setup.cfg [options]
```

### Command-Line Arguments

- --config, -c: Path to the config file (default: setup.cfg)
- --jira-server, -s: JIRA server address
- --jira-user, -u: JIRA user
- --jira-password, -p: JIRA password
- --jira-project: JIRA project key
- --jira-components: JIRA task components (comma-separated)
- --epic-link-field: ID of custom JIRA field for epic link
- --jira-epic: JIRA epic link
- --issue-type: JIRA issue type (default: 3)
- --planned-field: ID of custom JIRA field for planned date
- --duty_label: JIRA task label (default: flaky_duty)
- --dry-run: Dry run mode

### Example
```
python -m deflakyzavr -c setup.cfg --jira-server https://your-jira-server.com --jira-user your_username --jira-password your_password --jira-project your_project_key
```
