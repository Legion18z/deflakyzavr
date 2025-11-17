import datetime
import logging
from jira import JIRA, Issue

from deflakyzavr._jira_stdout import JiraUnavailable
from deflakyzavr._messages import RU_REPORTING_LANG

__all__ = ("deflakyzavration",)
logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s")


class CommentCleaner:
    def __init__(self, jira_client, jira_project,
                 dry_run=False,
                 flaky_ticket_label=None,
                 flaky_ticket_issue_types=None,
                 flaky_ticket_limit_comments_count=None,
                 flaky_ticket_allowed_comments_count=None,
                 flaky_ticket_deleted_comments_statuses=None,
                 flaky_ticket_weight_field_name=None,
                 flaky_ticket_weight_after_deleted_comments=None,
                 ) -> None:
        self._jira = jira_client
        self._jira_project = jira_project
        self._reporting_language = RU_REPORTING_LANG
        self._dry_run = dry_run
        self._flaky_ticket_label = flaky_ticket_label
        self._flaky_ticket_issue_types = flaky_ticket_issue_types
        self._flaky_ticket_limit_comments_count = flaky_ticket_limit_comments_count
        self._flaky_ticket_allowed_comments_count = flaky_ticket_allowed_comments_count
        self._flaky_ticket_deleted_comments_statuses = flaky_ticket_deleted_comments_statuses
        self._flaky_ticket_weight_field_name = flaky_ticket_weight_field_name
        self._flaky_ticket_weight_after_deleted_comments = flaky_ticket_weight_after_deleted_comments

    def _increase_ticket_weight(self, issue: Issue) -> None:
        custom_field_id = self._flaky_ticket_weight_field_name

        if not hasattr(issue.fields, custom_field_id):
            return

        current_value = getattr(issue.fields, custom_field_id)

        if isinstance(current_value, (int, float)):
            new_value = current_value + self._flaky_ticket_weight_after_deleted_comments
        elif current_value is None:
            new_value = self._flaky_ticket_weight_after_deleted_comments
        else:
            return

        issue.update(fields={custom_field_id: new_value})
        logging.warning(self._reporting_language.TICKET_WEIGHT_UPDATED.format(
            custom_field_id=issue.key, current_value=current_value, new_value=new_value,
        ))

    def _delete_comments(self, comments: list) -> None:
        for comment in comments:
            if comment.author.displayName != self._jira.jira_user_name:
                continue
            try:
                if not self._dry_run:
                    comment.delete()
                logging.warning(self._reporting_language.COMMENT_DELETED.format(
                    comment_id=comment.id, ticket_key=issue.key
                ))
            except Exception as e:
                logging.warning(self._reporting_language.COMMENT_DELETED_ERROR.format(
                    comment_id=comment.id, ticket_key=issue.key, error=e
                ))

    def delete_comments_in_flaky_tickets_with_not_allowed_comments_count(self) -> None:
        issue_types = ", ".join([f'{issue_type}' for issue_type in self._flaky_ticket_issue_types])
        issue_statuses = ", ".join([f'"{status}"' for status in self._flaky_ticket_deleted_comments_statuses])
        search_prompt = (
            f"project = {self._jira_project} "
            f"and issuetype in ({issue_types}) "
            f"and status in ({issue_statuses}) "
            f"and labels = {self._flaky_ticket_label} "
            f"and issueFunction in hasComments('+{self._flaky_ticket_allowed_comments_count}')"
        )

        found_issues = self._jira.search_issues(jql_str=search_prompt)
        if isinstance(found_issues, JiraUnavailable):
            logging.warning(
                self._reporting_language.SKIP_SEARCHING_TICKETS_DUE_TO_JIRA_SEARCH_UNAVAILABILITY.format(
                    jira_server=self._jira_server
                )
            )
            return

        for issue in found_issues:
            comments = issue.fields.comment.comments
            not_allowed_comments_number = len(comments) - self._flaky_ticket_allowed_comments_count

            if not_allowed_comments_number <= 0:
                return

            self._delete_comments(comments[:not_allowed_comments_number + self._flaky_ticket_limit_comments_count])
            logging.warning(self._reporting_language.TICKET_AFTER_DELETED_COMMENTS.format(
                ticket_key=issue.key
            ))

            if not self._dry_run:
                self.increase_ticket_weight(issue)


def comment_cleaner(jira_client, project, dry_run,
                    flaky_ticket_label=None,
                    flaky_ticket_issue_types=None,
                    flaky_ticket_allowed_comments_count=None,
                    flaky_ticket_limit_comments_count=None,
                    flaky_ticket_deleted_comments_statuses=None,
                    flaky_ticket_weight_field_name=None,
                    flaky_ticket_weight_after_deleted_comments=None,
                    ) -> None:
    comment_cleaner_client = CommentCleaner(
        jira_client=jira_client,
        jira_project=project,
        dry_run=dry_run,
        flaky_ticket_label = flaky_ticket_label,
        flaky_ticket_issue_types = flaky_ticket_issue_types,
        flaky_ticket_allowed_comments_count=flaky_ticket_allowed_comments_count,
        flaky_ticket_limit_comments_count=flaky_ticket_limit_comments_count,
        flaky_ticket_deleted_comments_statuses=flaky_ticket_deleted_comments_statuses,
        flaky_ticket_weight_field_name=flaky_ticket_weight_field_name,
        flaky_ticket_weight_after_deleted_comments=flaky_ticket_weight_after_deleted_comments,
    )
    comment_cleaner_client.delete_comments_in_flaky_tickets_with_not_allowed_comments_count()
