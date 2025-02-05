# deflakyzavr
Vedro plugin to simplify the duty of flaky tests
It requires the following arguments to run:
--jira-server         JIRA_SERVER, -s JIRA server address
--jira-user           JIRA_USER, -u JIRA user
--jira-password       JIRA_PASSWORD, -p JIRA password
--jira-project        JIRA project key
--epic-link-field     ID of custom JIRA field for epic link
--jira-epic           JIRA epic link
--issue-type          JIRA issue type
--planned-field       ID of custom JIRA field for planned date
--dry-run             Dry run mode

Example:
deflakyzavr -s {server-address} -u {username} -p {password} --jira-project {project-key}
--issue-type {ID of ticket type} --planned-field customfield_XXXXX --dry-run