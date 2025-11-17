import datetime
import logging

from jira import JIRA

from deflakyzavr._jira_stdout import LazyJiraTrier, JiraUnavailable
from deflakyzavr._messages import RU_REPORTING_LANG

__all__ = ("deflakyzavration",)
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")


class Deflakyzavr:
    def __init__(self, jira_client, jira_project,
                 issue_type=None, epic_link_field=None,
                 jira_components=None, jira_epic=None,
                 ticket_planned_field=None, duty_label=None,
                 dry_run=False,
                 flaky_ticket_label=None,
                 flaky_ticket_status=None,
                 flaky_ticket_link_type=None,
                 flaky_ticket_issue_types=None,
                 flaky_ticket_updated_days_ago=None,
                 ) -> None:
        self._jira: JIRA | LazyJiraTrier | None = jira_client
        self._jira_project = jira_project
        self._jira_issue_type = issue_type
        self._jira_components = jira_components
        self._jira_search_statuses = ['Взят в бэклог', 'Open']
        self._jira_search_forbidden_symbols = ['[', ']', '"']
        self._jira_duty_label = duty_label
        self._jira_epic_link_field = epic_link_field
        self._jira_epic = jira_epic
        self._reporting_language = RU_REPORTING_LANG
        self._jira_planned_field = ticket_planned_field
        self._dry_run = dry_run
        self._jira_flaky_ticket_label = flaky_ticket_label
        self._jira_flaky_ticket_status = flaky_ticket_status
        self._jira_flaky_ticket_link_type = flaky_ticket_link_type
        self._jira_flaky_ticket_issue_types = flaky_ticket_issue_types
        self._jira_flaky_ticket_updated_days_ago = flaky_ticket_updated_days_ago

    @staticmethod
    def _get_next_monday() -> datetime.date:
        today = datetime.date.today()
        days_ahead = 7 - today.weekday()
        if days_ahead == 0:
            days_ahead = 7
        next_monday = today + datetime.timedelta(days=days_ahead)
        return next_monday

    def _get_already_created_duty_ticket(self) -> str:
        issue_key = ''
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
            return 'jira_unavailable'
        elif found_issues:
            issue_key = found_issues[0].key  # type: ignore
            logging.warning(
                self._reporting_language.TICKET_ALREADY_EXISTS.format(jira_server=self._jira_server,
                                                                      issue_key=issue_key)
            )
        return issue_key

    def _format_ticket_fields(self) -> dict:
        planned_date = self._get_next_monday()
        issue_name = self._reporting_language.NEW_TICKET_SUMMARY.format(
            project_name=self._jira_project, planned_date=planned_date
        )
        ticket_fields = {
            'project': {'key': self._jira_project},
            'summary': issue_name,
            'issuetype': {'id': self._jira_issue_type if self._jira_issue_type else '3'},  # 3 is id for task
            'labels': [self._jira_duty_label],
        }
        if self._jira_components:
            ticket_fields['components'] = [{'name': component} for component in self._jira_components]
        if self._jira_epic_link_field and self._jira_epic:
            ticket_fields[self._jira_epic_link_field] = self._jira_epic
        if self._jira_planned_field:
            ticket_fields[self._jira_planned_field] = planned_date.isoformat()
        return ticket_fields

    def create_duty_ticket(self) -> str:
        issue_key = self._get_already_created_duty_ticket()

        if issue_key == 'jira_unavailable':
            return ''

        if issue_key == '':
            ticket_fields = self._format_ticket_fields()
            result_issue = self._jira.create_issue(fields=ticket_fields)
            if isinstance(result_issue, JiraUnavailable):
                logging.warning(
                    self._reporting_language.SKIP_CREATING_TICKET_DUE_TO_JIRA_CREATE_UNAVAILABILITY.format(
                        jira_server=self._jira_server
                    )
                )
                return ''

            issue_key = result_issue.key

        return issue_key

    def link_old_flaky_tickets_to_duty_ticket(self, duty_issue_key: str) -> None:
        issue_types = ", ".join([f'{issue_type}' for issue_type in self._jira_flaky_ticket_issue_types])
        search_prompt = (
            f"project = {self._jira_project} "
            f"and status = '{self._jira_flaky_ticket_status}' "
            f"and labels = {self._jira_flaky_ticket_label} "
            f"and (updated <= '-{self._jira_flaky_ticket_updated_days_ago}d' "
            f"or issueFunction in lastComment('before -{self._jira_flaky_ticket_updated_days_ago}d')) "
            f"and issuetype in ({issue_types}) "
            "ORDER BY created ASC"
        )

        found_issues = self._jira.search_issues(jql_str=search_prompt)
        if isinstance(found_issues, JiraUnavailable):
            logging.warning(
                self._reporting_language.SKIP_LINKING_TICKETS_DUE_TO_JIRA_SEARCH_UNAVAILABILITY.format(
                    jira_server=self._jira_server
                )
            )
            return

        for issue in found_issues:
            self._jira.create_issue_link(
                inwardIssue=issue.key,
                outwardIssue=duty_issue_key,
                linkType=self._jira_flaky_ticket_link_type
            )


def deflakyzavration(jira_client, project,
                     issue_type=None, epic_link_field=None, jira_epic=None,
                     jira_components=None, planned_field=None,
                     duty_label=None, dry_run=False,
                     flaky_ticket_label=None,
                     flaky_ticket_status=None,
                     flaky_ticket_link_type=None,
                     flaky_ticket_issue_types=None,
                     flaky_ticket_updated_days_ago=None,
                     ) -> None:
    client = Deflakyzavr(
        jira_client=jira_client,
        jira_project=project,
        jira_components=jira_components,
        epic_link_field=epic_link_field,
        jira_epic=jira_epic,
        issue_type=issue_type,
        ticket_planned_field=planned_field,
        duty_label=duty_label,
        dry_run=dry_run,
        flaky_ticket_label=flaky_ticket_label,
        flaky_ticket_status=flaky_ticket_status,
        flaky_ticket_link_type=flaky_ticket_link_type,
        flaky_ticket_issue_types=flaky_ticket_issue_types,
        flaky_ticket_updated_days_ago=flaky_ticket_updated_days_ago,
    )
    issue_key = client.create_duty_ticket()

    if issue_key:
        client.link_old_flaky_tickets_to_duty_ticket(issue_key)
