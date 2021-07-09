import json

from jira_project_config import JiraTypeIds


class CustomFields:
    FEATURE_FILE = "customfield_22100"
    SCENARIO_STEPS = "customfield_22114"
    SCENARIO_ORDER = "customfield_22109"


class TicketGenerator:
    def __init__(self, json_file):
        self.json_file = json_file
        self.bdd_data = None
        self.data_serialized = []

    def read_json(self):
        with open(self.json_file) as file:
            self.bdd_data = json.load(file)

    def feature_extraction(self, feature):
        issue_dict = {
            "project": {"key": JiraTypeIds.PROJECT_KEY},
            "summary": feature.get("Feature"),
            "issuetype": {"name": JiraTypeIds.FEATURE_TYPE_NAME},
            CustomFields.FEATURE_FILE: feature.get("FeatureFileName"),
        }

        return issue_dict

    def scenario_extraction(self, scenario):
        issue_dict = {
            "project": {"key": JiraTypeIds.PROJECT_KEY},
            "summary": scenario.get("Scenario"),
            "labels": scenario.get("Tags"),
            CustomFields.SCENARIO_STEPS: scenario.get("Steps"),
            CustomFields.SCENARIO_ORDER: float(scenario.get("scenarioId")),
            "issuetype": {"name": JiraTypeIds.SCENARIO_TYPE_NAME},
            "description": " ".join(scenario.get("images")),
        }
        return issue_dict

    def create_arr_by_feature(self):
        test_plan = []
        for feature in self.bdd_data:
            feature_and_scenarios = []
            feature_and_scenarios.append(self.feature_extraction(feature))
            for scenario in feature.get("Scenarios"):
                feature_and_scenarios.append(self.scenario_extraction(scenario))
            test_plan.append(feature_and_scenarios)

        return test_plan


if __name__ == "__main__":
    bdd = TicketGenerator("features.json")
    bdd.read_json()
    bdd.create_arr_by_feature()
