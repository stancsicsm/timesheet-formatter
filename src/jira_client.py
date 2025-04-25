import os
from dotenv import load_dotenv
from jira import JIRA

load_dotenv()


def get_jira_client():
    jira_server = os.getenv('JIRA_SERVER')
    jira_email = os.getenv('JIRA_EMAIL')
    jira_api_key = os.getenv('JIRA_API_KEY')
    if not jira_email or not jira_api_key:
        raise ValueError("JIRA_EMAIL or JIRA_API_KEY is not set in the environment variables.")
    return JIRA(jira_server, basic_auth=(jira_email, jira_api_key))
