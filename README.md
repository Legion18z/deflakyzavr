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
jira_token = jira_token
jira_project = your_project_key
jira_components = component1,component2
epic_link_field = customfield_10011
jira_epic = EPIC-123
issue_type = 3
planned_field = customfield_10012
duty_labels = flaky_duty,tech_debt_qa
dry_run = false
flaky_ticket_label= flaky
flaky_ticket_status = Backlog
flaky_ticket_link_type = 'has to be finished together with'
flaky_ticket_issue_types = 3,5,12900
flaky_ticket_updated_days_ago = 90
flaky_ticket_allowed_comments_count = 100
flaky_ticket_limit_comments_count = 30
flaky_ticket_deleted_comments_statuses = Взят в бэклог,Open,Reopened,In Progress,Code Review,Resolved
flaky_ticket_weight_field_name = customfield_38040
flaky_ticket_weight_after_deleted_comments = 101
```

## Usage
You can run the plugin using the following command:
```
python -m deflakyzavr --config path/to/setup.cfg [options]
```

### Command-Line Arguments

- --config, -c: Path to the config file (default: setup.cfg)
- --jira-server, -s: JIRA server address
- --jira-token, -t: JIRA token
- --jira-project: JIRA project key
- --jira-components: JIRA task components (comma-separated)
- --epic-link-field: ID of custom JIRA field for epic link
- --jira-epic: JIRA epic link
- --issue-type: JIRA issue type (default: 3)
- --planned-field: ID of custom JIRA field for planned date
- --duty_labels: JIRA task labels (default: flaky_duty,tech_debt_qa)
- --dry-run: Dry run mode
- --flaky-ticket-label: JIRA issue label for searching flaky tickets (default: flaky)
- --flaky-ticket-status: JIRA issue status for searching flaky tickets (default: 'Взят в бэклог')
- --flaky-ticket-link-type: JIRA issue link type for searching flaky tickets (default: 'has to be finished together with')
- --flaky-ticket-issue-types: JIRA issue types for searching flaky tickets (default: 3,5,12900)
- --flaky-ticket-updated-days-ago: Days ago jira issue was updated or its last comment for searching flaky tickets (default: 90)
- --flaky_ticket_allowed_comments_count: Allowed count of comments in ticket, above which comments will be deleted (default: 100)
- --flaky_ticket_limit_comments_count: Additional limit for deleting comments (default: 30)
- --flaky_ticket_deleted_comments_statuses: Statuses for searching tickets for deleting comments more than allowed count. Should be equal field jira_search_statuses in Flakyzavr (default: Взят в бэклог,Open,Reopened,In Progress,Code Review,Resolved)
- --flaky_ticket_weight_field_name: Field name to increase weight after deleting comments (default: customfield_38040)
- --flaky_ticket_weight_after_deleted_comments: Weight that will increase after deleting comments (default: 101)

### Example
Create setup.cfg and run command:
```
docker compose run app
```

Or if you need to redefine variables:
```
docker compose run app -c "python -m deflakyzavr --jira-server <jira_server> --jira-token <jira_token> -c setup.cfg"
```
