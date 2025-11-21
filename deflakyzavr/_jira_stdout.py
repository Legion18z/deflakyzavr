from collections import namedtuple
from json import JSONDecodeError as jsonJSONDecodeError
from typing import Any

from jira import Issue
from jira import JIRA
from jira import JIRAError
from requests import JSONDecodeError as requestsJSONDecodeError
from rtry import retry
import logging

MockIssue = namedtuple('MockIssue', ['key'])


class JiraAuthorizationError(BaseException):
    ...


class JiraUnavailable:
    ...


class LazyJiraTrier:
    def __init__(self, server, token, dry_run=False) -> None:
        self.server = server
        self._token = token
        self._jira = None
        self._dry_run = dry_run
        self.jira_user_names = None

    def connect(self) -> JIRA | JiraUnavailable:
        if not self._jira:
            try:
                self._jira = JIRA(server=self.server, token_auth=self._token)
                self.jira_user_names = [self._jira.myself()['displayName'], self._jira.myself()['name']]
            except JIRAError as e:
                logging.warning(e)
                if e.status_code == 403:
                    raise JiraAuthorizationError from None
                self._jira = None
                return JiraUnavailable()
            except jsonJSONDecodeError as e:
                logging.warning(e)
                self._jira = None
                return JiraUnavailable()
            except requestsJSONDecodeError as e:
                logging.warning(e)
                self._jira = None
                return JiraUnavailable()

        return self._jira

    def search_issues(self, jql_str: str) -> list[Issue] | JiraUnavailable:
        if self._dry_run:
            print(f'Query: {jql_str}')
        res = retry(delay=1, attempts=3, until=lambda x: isinstance(x, JiraUnavailable), logger=print)(self.connect)()
        if isinstance(res, JiraUnavailable):
            return res

        try:
            return retry(
                delay=1,
                attempts=3,
                swallow=(JIRAError, jsonJSONDecodeError, requestsJSONDecodeError)
            )(self._jira.search_issues)(jql_str=jql_str)
        except JIRAError as e:
            logging.warning(e)
            return JiraUnavailable()
        except jsonJSONDecodeError as e:
            logging.warning(e)
            return JiraUnavailable()
        except requestsJSONDecodeError as e:
            logging.warning(e)
            return JiraUnavailable()

    def create_issue(self, fields: dict[str, Any]) -> Issue | MockIssue | JiraUnavailable:
        res = retry(delay=1, attempts=3, until=lambda x: isinstance(x, JiraUnavailable), logger=print)(self.connect)()
        if isinstance(res, JiraUnavailable):
            return res

        if self._dry_run:
            print(f'Issue to create: {fields}')
            return MockIssue(key='EXISTING_MOCKED_ISSUE')

        try:
            issue = self._jira.create_issue(fields=fields)
        except JIRAError as e:
            logging.warning(e)
            return JiraUnavailable()
        except jsonJSONDecodeError as e:
            logging.warning(e)
            return JiraUnavailable()
        except requestsJSONDecodeError as e:
            logging.warning(e)
            return JiraUnavailable()
        return issue

    def create_issue_link(self, inwardIssue: str, outwardIssue: str,
                          linkType: str = 'is linked with') -> None | JiraUnavailable:
        res = retry(delay=1, attempts=3, until=lambda x: isinstance(x, JiraUnavailable), logger=print)(self.connect)()
        if isinstance(res, JiraUnavailable):
            return res

        if self._dry_run:
            print(f'Link {inwardIssue} with {outwardIssue}')
            return

        try:
            self._jira.create_issue_link(
                type=linkType,
                inwardIssue=inwardIssue,
                outwardIssue=outwardIssue
            )
        except JIRAError as e:
            logging.warning(e)
            return JiraUnavailable()
        except jsonJSONDecodeError as e:
            logging.warning(e)
            return JiraUnavailable()
        except requestsJSONDecodeError as e:
            logging.warning(e)
            return JiraUnavailable()
        return

    def add_comment(self, issue: Issue, text: str) -> list | JiraUnavailable:
        res = retry(delay=1, attempts=3, until=lambda x: isinstance(x, JiraUnavailable), logger=print)(self.connect)()
        if isinstance(res, JiraUnavailable):
            return res

        try:
            comments = self._jira.add_comment(issue, text)
        except JIRAError as e:
            logging.warning(e)
            return JiraUnavailable()
        except jsonJSONDecodeError as e:
            logging.warning(e)
            return JiraUnavailable()
        except requestsJSONDecodeError as e:
            logging.warning(e)
            return JiraUnavailable()

        return comments
