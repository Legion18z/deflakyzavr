import argparse
import sys
import logging
from typing import Any, Callable
from configparser import ConfigParser

from deflakyzavr._deflakyzavr_plugin import deflakyzavration
from deflakyzavr._comment_cleaner_plugin import comment_cleaner
from deflakyzavr._jira_stdout import LazyJiraTrier
from deflakyzavr._messages import RU_REPORTING_LANG


def read_config(config_file: str) -> ConfigParser:
    config = ConfigParser()
    config.read(config_file)
    return config


def make_param_getter(args: argparse.Namespace, config: ConfigParser, section: str = 'deflakyzavr') -> Callable:
    def get_param(name: str, default: Any = None) -> str:
        value = getattr(args, name)
        if value is not None:
            return value
        if config.has_option(section, name):
            return config.get(section, name)
        if default is not None:
            return default

        logging.error(RU_REPORTING_LANG.REQUIRED_PARAM_ERROR.format(name=name))
        sys.exit(1)
    return get_param


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a duty ticket in JIRA")
    parser.add_argument("--config", "-c", help="Path to config file", default="setup.cfg")

    # Основные параметры
    parser.add_argument("--jira-server", "-s", help="JIRA server address")
    parser.add_argument("--jira-token", "-t", help="JIRA token")
    parser.add_argument("--jira-project", help="JIRA project key")
    parser.add_argument("--jira-components", help="JIRA task components")
    parser.add_argument("--epic-link-field", help="ID of custom JIRA field for epic link")
    parser.add_argument("--jira-epic", help="JIRA epic link")
    parser.add_argument("--issue-type", help="JIRA issue type")
    parser.add_argument("--planned-field", help="ID of custom JIRA field for planned date")
    parser.add_argument("--duty_label", help="JIRA task label")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")

    # Flaky Ticket
    parser.add_argument("--flaky-ticket-label", help="JIRA issue label for searching flaky tickets")
    parser.add_argument("--flaky-ticket-status", help="JIRA issue status for searching flaky tickets")
    parser.add_argument("--flaky-ticket-link-type", help="JIRA issue link type for searching flaky tickets")
    parser.add_argument("--flaky-ticket-issue-types", help="JIRA issue types for searching flaky tickets")
    parser.add_argument("--flaky-ticket-updated-days-ago", help="Days ago jira issue was updated")

    # Comment Cleaner
    parser.add_argument("--flaky-ticket-allowed-comments-count", help="Allowed count of comments")
    parser.add_argument("--flaky-ticket-limit-comments-count", help="Additional limit for deleting comments")
    parser.add_argument("--flaky-ticket-deleted-comments-statuses", help="Statuses for deleting comments")
    parser.add_argument("--flaky-ticket-weight-field-name", help="Field name to increase weight")
    parser.add_argument("--flaky-ticket-weight-after-deleted-comments", help="Weight after deleting comments")

    args = parser.parse_args()
    config = read_config(args.config)

    get_param = make_param_getter(args, config)

    jira_server = get_param('jira_server')
    jira_token = get_param('jira_token')
    jira_project = get_param('jira_project')
    jira_components = get_param('jira_components')
    epic_link_field = get_param('epic_link_field')
    jira_epic = get_param('jira_epic')
    issue_type = get_param('issue_type')
    planned_field = get_param('planned_field')
    duty_label = get_param('duty_label')
    dry_run = args.dry_run or config.getboolean('deflakyzavr', 'dry_run', fallback=False)

    # Flaky Ticket
    flaky_ticket_label = get_param('flaky_ticket_label', default='flaky')
    flaky_ticket_status = get_param('flaky_ticket_status', default='Взят в бэклог')
    flaky_ticket_link_type = get_param('flaky_ticket_link_type', default='has to be finished together with')
    flaky_ticket_issue_types = get_param('flaky_ticket_issue_types', default=[3, 5, 12900])
    flaky_ticket_updated_days_ago = get_param('flaky_ticket_updated_days_ago', default=90)

    # Comment Cleaner
    flaky_ticket_allowed_comments_count = get_param('flaky_ticket_allowed_comments_count', default=100)
    flaky_ticket_limit_comments_count = get_param('flaky_ticket_limit_comments_count', default=30)
    flaky_ticket_deleted_comments_statuses = get_param(
        'flaky_ticket_deleted_comments_statuses',
        default=['Взят в бэклог', 'Open', 'Reopened', 'In Progress', 'Code Review', 'Resolved'])
    flaky_ticket_weight_field_name = get_param('flaky_ticket_weight_field_name', default='customfield_38040')
    flaky_ticket_weight_after_deleted_comments = get_param('flaky_ticket_weight_after_deleted_comments', default=101)

    jira_client = LazyJiraTrier(server=jira_server, token=jira_token, dry_run=dry_run)
    deflakyzavration(
        jira_client=jira_client,
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
    )

    comment_cleaner(
        jira_client=jira_client,
        project=jira_project,
        dry_run=dry_run,
        flaky_ticket_label=flaky_ticket_label,
        flaky_ticket_issue_types=flaky_ticket_issue_types,
        flaky_ticket_allowed_comments_count=flaky_ticket_allowed_comments_count,
        flaky_ticket_limit_comments_count=flaky_ticket_limit_comments_count,
        flaky_ticket_deleted_comments_statuses=flaky_ticket_deleted_comments_statuses,
        flaky_ticket_weight_field_name=flaky_ticket_weight_field_name,
        flaky_ticket_weight_after_deleted_comments=flaky_ticket_weight_after_deleted_comments,
    )