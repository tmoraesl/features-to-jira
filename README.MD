# What does it do

- Generate JSON and CSV from feature files
- Create tickets  configuration for each respective issuetype (Feature or Scenario)
- Create those tickets in jira
- Attach images in thumbnail format inside test steps
- Link all features to test plan
- Link all scenarios to its features and to test plan

# Setup environment

## Add your jira username and password in environment variables

**LINUX** 

``` 
# Open ~/.profile file and add at the end of the file
export TLF_JIRA_USERNAME=<YOUR_USER_NAME>
export TLF_JIRA_PASSWORD=<YOUR_PASSWORD>

# After saving changes, refresh file
source ~/.profile
```

**WINDOWS** 

[How To](https://docs.oracle.com/en/database/oracle/machine-learning/oml4r/1.5.1/oread/creating-and-modifying-environment-variables-on-windows.html#GUID-DD6F9982-60D5-48F6-8270-A27EC53807D0)
``` 
# Add these variables:
export TLF_JIRA_USERNAME=<YOUR_USER_NAME>
export TLF_JIRA_PASSWORD=<YOUR_PASSWORD>
```

## Create a virtual environment 

Create a directory in your machine and create a virtual environment

[How To Linux](https://www.youtube.com/watch?v=Kg1Yvry_Ydk&ab_channel=CoreySchafer)  
[How To Windows](https://www.youtube.com/watch?v=APOPm01BVrk&ab_channel=CoreySchafer)
``` 
#Virtual environment
# Create virtual environment
python3 -m venv venv

# Enable virtual environment in Linux
source venv/bin/activate

# Enable virtual environment in Windows
venv/Scripts/activate.bat
```

## Clone repository and install requirements   
Inside your project folder, clone this repo

Install requirements
``` 
pip install -r requirements.txt
```

# Structure

## Feature files blueprint

Expected this formatting inside feature files: [QA Features](https://docs-beta-living-apps.apps-dev.tid.es/docs/dev/qa)  
**Don't use Scenario Outline. For each case, create a single Scenario**

Besides basic feature files, we also add tags that will be added as labels and images to be added as thumbnails in our steps.

**Tags**  
`Tags: tag1, tag2, tag3`

**Image**  
`!image_<IMAGE_NAME>.png|thumbnail!`

**Example of a Fature and Scenario**
``` 
Feature: Access Living App
   Scenario: Access App with remote control in decoder
      Tags: uat, regression, desco
      Given: living apps screen is opened
      When: App living app is selected
      Then: initial screen of the living app is displayed
      !image_initial_screen.png|thumbnail!
```

**Important**
- Always leave **one blank** line between Scenarios
- Always finish feature file document **with two blank lines** to detec end of file
- See examples inside `features/` directory on this repo

**Add your reference images inside images directory**
- Store you reference images inside `images/` directory
- Image naming must follow the preset format `!image_<IMAGE_NAME>.png|thumbnail!`

## Project Settings

You must first create the Test Plan issue in jira by hand
Inside `jira_project_config.py` file add your test project key and test plan key created previously

```
class JiraTypeIds:
    PROJECT_KEY = "YOUR_PROJECT_KEY"
    TEST_PLAN_KEY = "YOUR_TES_PLAN_KEY"
```
Example:
```
class JiraTypeIds:
    PROJECT_KEY = "QALATEST"
    TEST_PLAN_KEY = "QALATEST-1"
```


# Running your script

- Enable your virtual environment
- Make sure your feature files are well formated as specified [here](#structure)
- You can use the feature files in this repo as examples
- You can run a single feature to test if everything is OK. Put the other features in another temporary folder and run the script, if everything is OK, move this one that was already created correctly and replace the rest of features in the feature folder
- Run the script: `python3 feature_to_jira.py`. This will run all the flow: covert .feature to json, create issue configurations, create tickets in jira, add images, add tags and link to parent feature/test plan