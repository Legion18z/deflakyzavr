import argparse
import configparser

from deflakyzavr._deflakyzavr_plugin import deflakyzavration

def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a duty ticket in JIRA")
    parser.add_argument("--config", "-c", help="Path to config file", default="setup.cfg")
    parser.add_argument("--jira-server", "-s", help="JIRA server address", default=None)
    parser.add_argument("--jira-user", "-u", help="JIRA user", default=None)
    parser.add_argument("--jira-password", "-p", help="JIRA password", default=None)
    parser.add_argument("--jira-project", help="JIRA project key", default=None)
    parser.add_argument("--jira-components", help="JIRA task components", default=None)
    parser.add_argument("--epic-link-field", help="ID of custom JIRA field for epic link", default=None)
    parser.add_argument("--jira-epic", help="JIRA epic link", default=None)
    parser.add_argument("--issue-type", help="JIRA issue type", default=None)
    parser.add_argument("--planned-field", help="ID of custom JIRA field for planned date", default=None)
    parser.add_argument("--duty_label", help="JIRA task label", default=None)
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    args = parser.parse_args()

    config = read_config(args.config)

    jira_server = args.jira_server or config.get('deflakyzavr', 'jira_server', fallback=None)
    jira_user = args.jira_user or config.get('deflakyzavr', 'jira_user', fallback=None)
    jira_password = args.jira_password or config.get('deflakyzavr', 'jira_password', fallback=None)
    jira_project = args.jira_project or config.get('deflakyzavr', 'jira_project', fallback=None)
    jira_components = args.jira_components or config.get('deflakyzavr', 'jira_components', fallback='')
    epic_link_field = args.epic_link_field or config.get('deflakyzavr', 'epic_link_field', fallback=None)
    jira_epic = args.jira_epic or config.get('deflakyzavr', 'jira_epic', fallback=None)
    issue_type = args.issue_type or config.get('deflakyzavr', 'issue_type', fallback='3')
    planned_field = args.planned_field or config.get('deflakyzavr', 'planned_field', fallback=None)
    duty_label = args.duty_label or config.get('deflakyzavr', 'duty_label', fallback='flaky_duty')
    dry_run = args.dry_run or config.getboolean('deflakyzavr', 'dry_run', fallback=False)

    deflakyzavration(
        server=jira_server,
        username=jira_user,
        password=jira_password,
        project=jira_project,
        epic_link_field=epic_link_field,
        jira_components=jira_components.split(','),
        jira_epic=jira_epic,
        issue_type=issue_type,
        planned_field=planned_field,
        duty_label=duty_label,
        dry_run=dry_run
    )