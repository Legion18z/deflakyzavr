import argparse

from deflakyzavr._deflakyzavr_plugin import found_and_create_duty_ticket

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a duty ticket in JIRA")
    parser.add_argument("--jira-server", "-s", required=True, help="JIRA server address")
    parser.add_argument("--jira-user", "-u", required=True, help="JIRA user")
    parser.add_argument("--jira-password", "-p", required=True, help="JIRA password")
    parser.add_argument("--jira-project", required=True, help="JIRA project key")
    parser.add_argument("--epic-link-field", required=False, help="ID of custom JIRA field for epic link")
    parser.add_argument("--jira-epic", required=False, help="JIRA epic link")
    parser.add_argument("--issue-type", required=False, help="JIRA issue type", default='3')
    parser.add_argument("--planned-field", required=False, help="ID of custom JIRA field for planned date")
    parser.add_argument("--dry-run", required=False, action="store_true", help="Dry run mode")
    args = parser.parse_args()

    found_and_create_duty_ticket(
        server=args.jira_server,
        username=args.jira_user,
        password=args.jira_password,
        project=args.jira_project,
        epic_link_field=args.epic_link_field,
        jira_epic=args.jira_epic,
        issue_type=args.issue_type,
        planned_field=args.planned_field,
        dry_run=args.dry_run
    )
