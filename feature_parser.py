import os
import csv
import json
import re
import logging

logger = logging.getLogger(__name__)


class ReadFeatureFiles:
    """Read feature files and parse information to generate different files
    Expects filenames to be "<3-digt-id>_<feature_name>.feature"
    Example: 001_access_application.feature

    File content must follow the Telefonica BDD format but also allows image reference
        to attach in a scenario step:

    Feature: Access App
        Scenario: Access app with remote control in decoder
            Tags: uat, regression, desco
            Given: app screen is opened
            When: app is selected
            Then: initial screen of the app is displayed
            !image_<IMG_NAME>.png|thumbnail!

    """

    def __init__(self, features_dir):
        """Initialize class with files containing the features

        Args:
            features_dir (str): Feature files directory
        """
        self.feature_files = []
        self.feature_id = []
        self.features_dir = features_dir

    def feature_files_list(self):
        """Get list of feature files and store their names
        Split feature if from file name

        Raises:
            FileNotFoundError: If no features are found
        """
        for file in os.listdir(self.features_dir):
            if file.endswith(".feature"):
                self.feature_files.append(file)
                self.feature_id.append(file.split("_")[0])
        if not self.feature_files.append:
            raise FileNotFoundError(
                f"No *.feature files found in directory {self.features_dir}"
            )

    def read_feature_file(self, file):
        """Returns a list of each line in file

        Args:
            file (feature): feature file

        Returns:
            list: list containing each line in feature file
        """
        with open(self.features_dir + file) as f:
            return f.readlines()

    def get_feature(self, content):
        """Removes empty space and returns feature name

        Args:
            content (str): string containing feature name

        Returns:
            str: feature name
        """
        for line in content:
            if "Feature:" in line:
                return line.replace("\n", " ").replace("\r", "").split("Feature: ")[1]

    def get_scenario(self, scenario):
        """Removes empty space and returns scenario name

        Args:
            content (str): string containing scenario name

        Returns:
            str: scenario name
        """
        if "Outline" in scenario:
            return (
                scenario.replace("\n", " ")
                .replace("  ", "")
                .split("Scenario Outline: ")[1]
            )
        else:
            return scenario.replace("\n", " ").replace("  ", "").split("Scenario: ")[1]

    def is_outline(self, scenario):
        """Check if is scenario outline

        Args:
            scenario (str): scenario name

        Returns:
            bool: True if is scenario outlone
        """
        return True if "Scenario Outline" in scenario else False

    def get_tags(self, tags):
        """Return list of tags

        Args:
            tags (str): list of tags divided by comma

        Returns:
            list: list of strings of tags
        """
        t = tags.split("Tags: ")[1].strip("\n")
        return t.split(", ")

    def convert_tags_list_to_str(self, tags):
        """Convert tag list to string to add in another file format
        Such as csv or docx

        Args:
            tags (list): list of tags

        Returns:
            [str]: string of tags divided by comma
        """
        return ", ".join(tags)

    def get_steps(self, steps):
        """Remove spaces from steps

        Args:
            steps (str): Steps

        Returns:
            str: Steps without formatting spaces
        """
        return steps.replace("    ", " ")

    def get_image(self, image):
        """Remove spaces from image

        Args:
            image (str): image

        Returns:
            str: image without formatting spaces
        """
        img = image.replace("    ", " ")
        return img

    def get_image_file_name(self, img):
        """Finds name of the image file using reguar expression

        Args:
            img (string): name of image tag in jira format

        Raises:
            ValueError: Image not found

        Returns:
            str: name of the image file to be searched in images directory
        """
        fname = re.search("[A-z_0-9]+.(png|jpg|jpeg)", img)

        if fname:
            return fname.group()
        else:
            raise ValueError(
                "Expected: !image_<IMG_NAME>.png|thumbnail!"
            )

    def parse_content(self, content):
        """Reads feature file line by line and check if if
        - Is feature name
        - Is scenario name
        - Are tags
        - Are steps
        - Are images
        - Are scenario outlines
        - Are examples

        Args:
            content (string): line from feature file

        Returns:
            dictionary: formatted content dictionary
        """
        parse_content = {}
        scenarios = []
        scenario = {}
        steps = []
        images = []
        bdd_keys = ["Given:", "When:", "Then:", "And:", "But:"]
        is_outline = False
        scenario_id = 0

        parse_content["Feature"] = self.get_feature(content)

        for line in content:
            if "Scenario:" in line:
                scenario["Scenario"] = self.get_scenario(line)
                is_outline = self.is_outline(line)
            elif "Tags:" in line:
                scenario["Tags"] = self.get_tags(line)
            elif any(x in line for x in bdd_keys):
                steps.append(self.get_steps(line))
            elif "!image_" in line:
                img = self.get_image(line)
                steps.append(img)
                images.append(self.get_image_file_name(img))
            elif "Examples" in line:
                steps.append(line)
            elif "|" in line:
                steps.append(line)
            elif len(line.strip()) == 0:
                if is_outline:
                    steps.append(line)
                    is_outline = False
                else:
                    scenario["Steps"] = "".join(steps)
                    scenario_id = scenario_id + 1
                    scenario["scenarioId"] = scenario_id
                    scenario["images"] = images
                    scenarios.append(scenario)
                    scenario = {}
                    steps = []
                    images = []

        parse_content["Scenarios"] = scenarios

        return parse_content


class RowParser:
    """Create headers and rows for csv file
    """
    def __init__(self, data):
        self.data = data

    def parse_row(self):
        rows = []

        for element in self.data:
            for scenario in element["Scenarios"]:
                row = []
                row.append(element.get("FeatureId"))
                row.append(scenario.get("scenarioId"))
                row.append(element.get("Feature"))
                row.append(scenario.get("Scenario"))
                row.append(scenario.get("Tags"))
                row.append(scenario.get("Steps"))
                rows.append(row)

        return rows


class CSVWriter:
    """Generates csv file
    """

    filename = None
    fp = None
    writer = None

    def __init__(self, filename):
        self.filename = filename
        self.fp = open(self.filename, "w", encoding="utf8")
        self.writer = csv.writer(
            self.fp,
            delimiter=";",
            quotechar='"',
            quoting=csv.QUOTE_ALL,
            lineterminator="\n",
        )

    def close(self):
        self.fp.close()

    def write(self, elems):
        self.writer.writerow(elems)

    def size(self):
        return os.path.getsize(self.filename)

    def fname(self):
        return self.filename


class ParseMetadata:
    """Main class that generates json and csv files from feature files and images
    """
    def __init__(
        self, features_dir, json_fname="features.json", csv_fname="TestPlan.csv"
    ):
        self.features_dir = features_dir
        self.ordered_features = None
        self.json_fname = json_fname
        self.csv_fname = csv_fname

    def parse_metadata(self):
        read = ReadFeatureFiles(self.features_dir)
        read.feature_files_list()
        features = []
        for index, fname in enumerate(read.feature_files):
            content = read.read_feature_file(fname)
            parsed = read.parse_content(content)
            parsed["FeatureId"] = int(read.feature_id[index])
            parsed["FeatureFileName"] = fname
            features.append(parsed)

        self.ordered_features = sorted(features, key=lambda k: k["FeatureId"])

    def generate_json(self):
        with open(self.json_fname, "w") as f:
            f.write(json.dumps(self.ordered_features))

    def generate_csv(self):
        row_parser = RowParser(self.ordered_features)
        rows = row_parser.parse_row()

        mycsv = CSVWriter(self.csv_fname)
        mycsv.write(("FeatureId", "ScenarioId", "Feature", "Scenario", "Tags", "Steps"))
        for row in rows:
            mycsv.write(row)
        mycsv.close()


if __name__ == "__main__":
    parser = ParseMetadata("features/")
    parser.parse_metadata()
    parser.generate_json()
    parser.generate_csv()
