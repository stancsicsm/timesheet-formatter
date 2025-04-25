import sys
from jira_client import get_jira_client
from utils import get_content_by_days, get_epics_with_stories, get_grouped_epics_by_day, print_formatted_output

jira = get_jira_client()

print("Please paste your data below. Press Ctrl+D (Ctrl+Z on Windows) to finish:")
content = sys.stdin.read().strip()
print("Processing...")

content_by_days = get_content_by_days(content)
story_keys = {story[0] for stories_with_time in content_by_days.values() for story in stories_with_time}
epics_with_stories = get_epics_with_stories(jira, story_keys)
epics_by_day = get_grouped_epics_by_day(content_by_days, epics_with_stories)

print_formatted_output(epics_by_day)
