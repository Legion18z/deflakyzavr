from typing import NamedTuple


class ReportingLangSet(NamedTuple):
    SKIP_CREATING_TICKET_DUE_TO_JIRA_SEARCH_UNAVAILABILITY: str
    SKIP_CREATING_TICKET_DUE_TO_JIRA_CREATE_UNAVAILABILITY: str
    SKIP_LINKING_TICKETS_DUE_TO_JIRA_SEARCH_UNAVAILABILITY: str
    TICKET_ALREADY_EXISTS: str
    TICKET_CREATED: str
    RELATED_TICKETS_FOUND: str
    NEW_TICKET_SUMMARY: str
    SKIP_SEARCHING_TICKETS_DUE_TO_JIRA_SEARCH_UNAVAILABILITY: str
    COMMENT_DELETED: str
    COMMENT_DELETED_ERROR: str
    TICKET_AFTER_DELETED_COMMENTS: str
    TICKET_WEIGHT_UPDATED: str
    TICKET_COMMENT_AFTER_DELETED_COMMENTS: str
    REQUIRED_PARAM_ERROR: str


RU_REPORTING_LANG = ReportingLangSet(
    SKIP_CREATING_TICKET_DUE_TO_JIRA_SEARCH_UNAVAILABILITY=(
        '{jira_server} не был доступен во время поиска тикетов. '
        'Пропускаем создание тикета'
    ),
    SKIP_CREATING_TICKET_DUE_TO_JIRA_CREATE_UNAVAILABILITY=(
        '{jira_server} не был доступен во время создания тикета. '
        'Пропускаем создание тикета'
    ),
    SKIP_LINKING_TICKETS_DUE_TO_JIRA_SEARCH_UNAVAILABILITY=(
        '{jira_server} не был доступен во время поиска тикетов. '
        'Пропускаем слинкование тикетов'
    ),
    SKIP_SEARCHING_TICKETS_DUE_TO_JIRA_SEARCH_UNAVAILABILITY=(
        '{jira_server} не был доступен во время поиска тикетов. '
        'Пропускаем поиск тикетов'
    ),
    TICKET_ALREADY_EXISTS='Тикет дежурства уже есть {jira_server}/browse/{issue_key}',
    TICKET_CREATED='Заведен новый тикет дежурства {jira_server}/browse/{issue_key}',
    RELATED_TICKETS_FOUND='Есть связанные c этим файлом тикеты: {issues}',
    NEW_TICKET_SUMMARY='[{project_name}] Флаки дежурство {planned_date}',
    COMMENT_DELETED='Комментарий {comment_id} удалён из тикета {ticket_key}',
    COMMENT_DELETED_ERROR='Комментарий {comment_id} не был удалён из тикета {ticket_key} из-за ошибки {error}',
    TICKET_AFTER_DELETED_COMMENTS='Тикет {ticket_key} был обработан из-за превышающего кол-ва комментариев',
    TICKET_WEIGHT_UPDATED='Вес задачи обновлён: {current_value} → {new_value}',
    TICKET_COMMENT_AFTER_DELETED_COMMENTS='Было удалено {deleted_comments_count} комментариев. '
                                          'Вес задачи увеличен на {weight}.',
    REQUIRED_PARAM_ERROR = 'Обязательный параметр {name} не найден ни в конфигурации, ни в аргументах командной строки.'
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
    SKIP_LINKING_TICKETS_DUE_TO_JIRA_SEARCH_UNAVAILABILITY=(
        '{jira_server} was unavailable while searching for issues. '
        'Skip tickets linking.'
    ),
    SKIP_SEARCHING_TICKETS_DUE_TO_JIRA_SEARCH_UNAVAILABILITY=(
        '{jira_server} was unavailable while searching for issues. '
        'Skip searching tickets.'
    ),
    TICKET_ALREADY_EXISTS='Ticket for duty task already exists: {jira_server}/browse/{issue_key}',
    TICKET_CREATED='Ticket for duty task created: {jira_server}/browse/{issue_key}',
    RELATED_TICKETS_FOUND='Found related issues by test file: {issues}',
    NEW_TICKET_SUMMARY='[{project_name}] Flaky duty',
    COMMENT_DELETED='Comment {comment_id} has been removed from ticket {ticket_key}',
    COMMENT_DELETED_ERROR='Comment {comment_id} was not removed from ticket {ticket_key} due to error {error}',
    TICKET_AFTER_DELETED_COMMENTS='Ticket {ticket_key} was processed due to excessive number of comments',
    TICKET_WEIGHT_UPDATED='The task weight has been updated: {current_value} → {new_value}',
    TICKET_COMMENT_AFTER_DELETED_COMMENTS='{deleted_comments_count} comments were deleted. '
                                          'Task weight increased by {weight}.',
    REQUIRED_PARAM_ERROR='Required parameter {name} was not found in either the configuration or '
                         'the command line arguments.'
)
