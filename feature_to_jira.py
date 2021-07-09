from feature_parser import ParseMetadata
from ticket_gen import TicketGenerator
from jira_tlf import TelefonicaJira
from jira_project_config import JiraTypeIds

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

# Path and file names
FEATURE_DIR = "features/"
IMAGE_DIR = "images/"
JSON_FNAME = "features.json"


# Generate Json from feature files inside FEATURE_DIR
parser = ParseMetadata(FEATURE_DIR, json_fname=JSON_FNAME)
parser.parse_metadata()
parser.generate_json()

# Read json file and create the issue_dict for each issue type
# Generate list of lists. Each list contains a single feature and its scenarios
bdd = TicketGenerator(JSON_FNAME)
bdd.read_json()
test_plan = bdd.create_arr_by_feature()

# Connect to jira and get jira object
tlf = TelefonicaJira()


def create_feature(issues):
    for issue in issues:
        if issue.get("issuetype").get("name") == "Feature":
            logger.info(f"Will create: {issue.get('issuetype').get('name')}")
            logger.info(f"Summary: {issue.get('summary')}")
            feature = tlf.create_ticket(issue)
            tlf.create_link(
                JiraTypeIds.TEST_PLAN_TYPE_NAME, JiraTypeIds.TEST_PLAN_KEY, feature.key
            )
            return feature


def create_scenarios(issues, feature):
    for issue in issues:
        if issue.get("issuetype").get("name") == "Scenario":
            logger.info(f"Will create: {issue.get('issuetype').get('name')}")
            logger.info(f"Summary: {issue.get('summary')}")
            scenario = tlf.create_ticket(issue)
            tlf.create_link(
                JiraTypeIds.TEST_PLAN_TYPE_NAME, JiraTypeIds.TEST_PLAN_KEY, scenario.key
            )
            tlf.create_link(JiraTypeIds.FEATURE_TYPE_NAME, feature.key, scenario.key)

            attatch_images(scenario, issue.get("description").split())


def attatch_images(issue, imgs):
    if not imgs:
        return
    else:
        for img in imgs:
            fpath = IMAGE_DIR + img
            tlf.attatch_file(issue, fpath)

if __name__ == "__main__":
    # Iterate through the testplan
    for issues in test_plan:
        feature = create_feature(issues)
        create_scenarios(issues, feature)
