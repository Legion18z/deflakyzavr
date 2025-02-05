from typing import NamedTuple


class ReportingLangSet(NamedTuple):
    SKIP_CREATING_TICKET_DUE_TO_JIRA_SEARCH_UNAVAILABILITY: str
    SKIP_CREATING_TICKET_DUE_TO_JIRA_CREATE_UNAVAILABILITY: str
    TICKET_ALREADY_EXISTS: str
    TICKET_CREATED: str
    RELATED_TICKETS_FOUND: str
    NEW_TICKET_SUMMARY: str
    NEW_TICKET_TEXT: str


RU_REPORTING_LANG = ReportingLangSet(
    SKIP_CREATING_TICKET_DUE_TO_JIRA_SEARCH_UNAVAILABILITY=(
        '{jira_server} не был доступен во время поиска тикетов. '
        'Пропускаем создание тикета'
    ),
    SKIP_CREATING_TICKET_DUE_TO_JIRA_CREATE_UNAVAILABILITY=(
        '{jira_server} не был доступен во время создания тикета. '
        'Пропускаем создание тикета'
    ),
    TICKET_ALREADY_EXISTS='Тикет дежурства уже есть {jira_server}/browse/{issue_key}',
    TICKET_CREATED='Заведен новый тикет дежурства {jira_server}/browse/{issue_key}',
    RELATED_TICKETS_FOUND='Есть связанные c этим файлом тикеты: {issues}',
    NEW_TICKET_SUMMARY='[{project_name}] Флаки дежурство {planned_date}',
    NEW_TICKET_TEXT=(
        'h2. Контекст\n'
        'Этот тикет заведен для флаки дежурства, к нему будут линковаться все заводящиеся флаки тикеты '
        'на период дежурства\n'
    )
)

EN_REPORTING_LANG = ReportingLangSet(
    SKIP_CREATING_TICKET_DUE_TO_JIRA_SEARCH_UNAVAILABILITY=(
        '{jira_server} was unavailable while searching for issues. '
        'Skip ticket creating.'
    ),
    SKIP_CREATING_TICKET_DUE_TO_JIRA_CREATE_UNAVAILABILITY=(
        '{jira_server} was unavailable while creating issue. '
        'Skip ticket creating.'
    ),
    TICKET_ALREADY_EXISTS='Ticket for duty task already exists: {jira_server}/browse/{issue_key}',
    TICKET_CREATED='Ticket for duty task created: {jira_server}/browse/{issue_key}',
    RELATED_TICKETS_FOUND='Found related issues by test file: {issues}',
    NEW_TICKET_SUMMARY='[{project_name}] Flaky duty',
    NEW_TICKET_TEXT=(
        'h2. {{color:#172b4d}}Context{{color}}\n'
        'Flaky duty: \n'
        'h2. {{color:#172b4d}}Steps to do:{{color}}\n'
        '{{task}}Skip flaky test in repo{{task}}\n'
        '{{task}}Fix fail cause{{task}}\n'
        '{{task}}Check test priority(in test and ticket){{task}}\n'
        '{{task}}Skip fail by expected_failure plugin{{task}}\n'
        '{{task}}Fix unstable test{{task}}'
    )
)
