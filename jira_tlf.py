import os
from jira import JIRA, JIRAError
import logging

logger = logging.getLogger(__name__)


class TelefonicaJira:
    def __init__(self):
        self.jira = self._connect_to_tlf_jira(
            os.environ["TLF_JIRA_USERNAME"], os.environ["TLF_JIRA_PASSWORD"]
        )

    def _connect_to_tlf_jira(self, username, password):
        jira_server = "https://jira.tid.es"
        jira_options = {"server": jira_server}
        logger.info(">>>> Connecting to TLF JIRA")
        try:
            jira = JIRA(options=jira_options, basic_auth=(username, password))
        except Exception as e:
            logger.error("Cant connect to Jira: " + str(e))
            quit()
        else:
            return jira

    def get_issue_information(self, issue_id):
        try:
            issue = self.jira.issue(issue_id)
            logger.info(f"Reading {issue.key}")
            return issue
        except JIRAError:
            return None

        # Issue Type Id
        issue_id = issue.fields.issuetype.id
        logger.info(f"id: {issue_id}")
        # Issue Key
        issue_key = issue.key
        logger.info(f"key: {issue_key}")
        # Issue Summary
        issue_summary = issue.fields.summary
        logger.info(f"summary: {issue_summary}")
        # Issue Labels
        labels = issue.fields.labels
        logger.info(f"labels: {labels}")

        for link in issue.fields.issuelinks:
            if hasattr(link, "outwardIssue"):
                outward_issue = link.outwardIssue
                logger.info("Children:")
                logger.info(f"\ttype_id: {link.type.id}")
                logger.info(f"\tname: {link.type.name}")
                logger.info(f"\tkey: {outward_issue.key}")
            if hasattr(link, "inwardIssue"):
                inward_issue = link.inwardIssue
                logger.info("Parent:")
                logger.info(f"\ttype_id: {link.type.id}")
                logger.info(f"\tname: {link.type.name}")
                logger.info(f"\tkey: {inward_issue.key}")

    def create_ticket(self, ticket):
        issue = self.jira.create_issue(ticket)
        logger.info(f"Created {issue.key}")
        return issue

    def create_link(self, type, inward_issue, outward_issue):
        logger.info(f"Linking {type} parent {inward_issue} children {outward_issue}")
        return self.jira.create_issue_link(type, inward_issue, outward_issue)

    def attatch_file(self, issue, fpath):
        try:
            logger.info(f"Attaching {fpath} to {issue}")
            self.jira.add_attachment(issue=issue, attachment=fpath)
        except Exception as e:
            logger.error(f"{e}: Not possible to attach {fpath} to {issue}")


if __name__ == "__main__":
    tlf = TelefonicaJira()
    tlf.get_issue_information("QALARN-3")
