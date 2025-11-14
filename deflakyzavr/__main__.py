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
    parser.add_argument("--jira-token", "-t", help="JIRA token", default=None)
    parser.add_argument("--jira-project", help="JIRA project key", default=None)
    parser.add_argument("--jira-components", help="JIRA task components", default=None)
    parser.add_argument("--epic-link-field", help="ID of custom JIRA field for epic link", default=None)
    parser.add_argument("--jira-epic", help="JIRA epic link", default=None)
    parser.add_argument("--issue-type", help="JIRA issue type", default=None)
    parser.add_argument("--planned-field", help="ID of custom JIRA field for planned date", default=None)
    parser.add_argument("--duty_label", help="JIRA task label", default=None)
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    parser.add_argument("--flaky-ticket-label", help="JIRA issue label for searching flaky tickets", default='flaky')
    parser.add_argument("--flaky-ticket-status", help="JIRA issue status for searching flaky tickets",
                        default='Взят в бэклог')
    parser.add_argument("--flaky-ticket-link-type", help="JIRA issue link type for searching flaky tickets",
                        default='has to be finished together with')
    parser.add_argument("--flaky-ticket-issue-types", help="JIRA issue types for searching flaky tickets",
                        default=[3, 5, 12900])
    parser.add_argument("--flaky-ticket-updated-days-ago",
                        help="Days ago jira issue was updated or its last comment for searching flaky tickets",
                        default='90')
    parser.add_argument("--flaky-ticket-allowed-comments-count",
                        help="Allowed count of comments in ticket, above which comments will be deleted",
                        default=100)
    args = parser.parse_args()

    config = read_config(args.config)

    jira_server = args.jira_server or config.get('deflakyzavr', 'jira_server', fallback=None)
    jira_token = args.jira_token or config.get('deflakyzavr', 'jira_token', fallback=None)
    jira_project = args.jira_project or config.get('deflakyzavr', 'jira_project', fallback=None)
    jira_components = args.jira_components or config.get('deflakyzavr', 'jira_components', fallback='')
    epic_link_field = args.epic_link_field or config.get('deflakyzavr', 'epic_link_field', fallback=None)
    jira_epic = args.jira_epic or config.get('deflakyzavr', 'jira_epic', fallback=None)
    issue_type = args.issue_type or config.get('deflakyzavr', 'issue_type', fallback='3')
    planned_field = args.planned_field or config.get('deflakyzavr', 'planned_field', fallback=None)
    duty_label = args.duty_label or config.get('deflakyzavr', 'duty_label', fallback='flaky_duty')
    dry_run = args.dry_run or config.getboolean('deflakyzavr', 'dry_run', fallback=False)
    flaky_ticket_label = args.flaky_ticket_label or config.get('deflakyzavr', 'flaky_ticket_label', fallback=None)
    flaky_ticket_status = args.flaky_ticket_status or config.get('deflakyzavr', 'flaky_ticket_status', fallback=None)
    flaky_ticket_link_type = args.flaky_ticket_link_type or config.get(
        'deflakyzavr', 'flaky_ticket_link_type', fallback=None)
    flaky_ticket_issue_types = args.flaky_ticket_issue_types or config.get(
        'deflakyzavr', 'flaky_ticket_issue_types', fallback=None)
    flaky_ticket_updated_days_ago = args.flaky_ticket_updated_days_ago or config.get(
        'deflakyzavr', 'flaky_ticket_updated_days_ago', fallback=None)
    flaky_ticket_allowed_comments_count = args.flaky_ticket_allowed_comments_count or config.get(
        'deflakyzavr', 'flaky_ticket_allowed_comments_count', fallback=None)

    deflakyzavration(
        server=jira_server,
        token=jira_token,
        project=jira_project,
        epic_link_field=epic_link_field,
        jira_components=jira_components.split(','),
        jira_epic=jira_epic,
        issue_type=issue_type,
        planned_field=planned_field,
        duty_label=duty_label,
        dry_run=dry_run,
        flaky_ticket_label=flaky_ticket_label,
        flaky_ticket_status=flaky_ticket_status,
        flaky_ticket_link_type=flaky_ticket_link_type,
        flaky_ticket_issue_types=flaky_ticket_issue_types,
        flaky_ticket_updated_days_ago=flaky_ticket_updated_days_ago,
        flaky_ticket_allowed_comments_count=flaky_ticket_allowed_comments_count,
    )