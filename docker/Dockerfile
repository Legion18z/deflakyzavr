FROM python:3.12.8-alpine3.20
LABEL description="Deflakyzavr (https://github.com/Legion18z/deflakyzavr) plugin. \
Env params should be set up: \
- JIRA_SERVER - jira server address; \
- JIRA_USER - jira user; \
- JIRA_PASSWORD - jira password; \
- JIRA_PROJECT - jira space for project or command; \
- JIRA_ISSUE_TYPE_ID - jira issue type ID (default = 3 (Task)); \
- JIRA_PLANNED_FIELD - optional param for custom field for planned date; \
"

WORKDIR /deflakyzavr
ADD . .

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

RUN python3 -m pip install .

CMD ["sh", "-c", "deflakyzavr"]