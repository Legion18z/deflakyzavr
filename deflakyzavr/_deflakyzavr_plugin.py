import datetime
import logging

from jira import JIRA

from deflakyzavr._jira_stdout import LazyJiraTrier, JiraUnavailable
from deflakyzavr._messages import RU_REPORTING_LANG

__all__ = ("found_and_create_duty_ticket",)
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")


class Deflakyzavr:
    def __init__(self, jira_server, username, password, jira_project,
                 issue_type=None, epic_link_field=None, jira_epic=None,
                 ticket_planned_field=None, dry_run=False) -> None:
        self._jira_server = jira_server
        self._jira_user = username
        self._jira_password = password
        self._jira_project = jira_project
        self._jira_issue_type = issue_type
        self._jira_components = ['all']
        self._jira: JIRA | LazyJiraTrier | None = None
        self._jira_search_statuses = ['Взят в бэклог', 'Open']
        self._jira_search_forbidden_symbols = ['[', ']', '"']
        self._jira_duty_label = 'flaky_duty'
        self._jira_epic_link_field = epic_link_field
        self._jira_epic = jira_epic
        self._reporting_language = RU_REPORTING_LANG
        self._jira_planned_field = ticket_planned_field
        self._dry_run = dry_run

    @staticmethod
    def _get_next_monday() -> datetime.date:
        today = datetime.date.today()
        days_ahead = 7 - today.weekday()
        if days_ahead == 0:
            days_ahead = 7
        next_monday = today + datetime.timedelta(days=days_ahead)
        return next_monday

    def create_duty_ticket(self) -> None:
        self._jira = LazyJiraTrier(
            self._jira_server,
            basic_auth=(self._jira_user, self._jira_password),
            dry_run=self._dry_run
        )

        statuses = ",".join([f'"{status}"' for status in self._jira_search_statuses])
        search_prompt = (
            f'project = {self._jira_project} '
            f'and status in ({statuses}) '
            f'and labels = {self._jira_duty_label} '
            'ORDER BY created'
        )

        found_issues = self._jira.search_issues(jql_str=search_prompt)
        if isinstance(found_issues, JiraUnavailable):
            logging.warning(
                self._reporting_language.SKIP_CREATING_TICKET_DUE_TO_JIRA_SEARCH_UNAVAILABILITY.format(
                    jira_server=self._jira_server
                )
            )
            return

        if found_issues:
            issue = found_issues[0]  # type: ignore
            logging.warning(
                self._reporting_language.TICKET_ALREADY_EXISTS.format(jira_server=self._jira_server, issue_key=issue.key)
            )
            return
        planned_date = self._get_next_monday()
        issue_name = self._reporting_language.NEW_TICKET_SUMMARY.format(
            project_name=self._jira_project, planned_date=planned_date
        )
        issue_description = self._reporting_language.NEW_TICKET_TEXT
        created_ticket_fields = {
                'project': {'key': self._jira_project},
                'summary': issue_name,
                'description': issue_description,
                'issuetype': {'id': self._jira_issue_type if self._jira_issue_type else '3'},   # 3 is id for task
                'components': [{'name': component} for component in self._jira_components],
                'labels': [self._jira_duty_label],
            }
        if self._jira_epic_link_field and self._jira_epic:
            created_ticket_fields[self._jira_epic_link_field] = self._jira_epic
        if self._jira_planned_field:
            created_ticket_fields[self._jira_planned_field] = planned_date.isoformat()
        result_issue = self._jira.create_issue(fields=created_ticket_fields)
        if isinstance(result_issue, JiraUnavailable):
            logging.warning(
                self._reporting_language.SKIP_CREATING_TICKET_DUE_TO_JIRA_CREATE_UNAVAILABILITY.format(
                    jira_server=self._jira_server
                )
            )
            return


def found_and_create_duty_ticket(server, username, password, project,
                                 issue_type=None, epic_link_field=None, jira_epic=None,
                                 planned_field=None, dry_run=False) -> None:

    client = Deflakyzavr(
        jira_server=server,
        username=username,
        password=password,
        jira_project=project,
        epic_link_field=epic_link_field,
        jira_epic=jira_epic,
        issue_type=issue_type,
        ticket_planned_field=planned_field,
        dry_run=dry_run
    )
    client.create_duty_ticket()
