import re


def to_float(value):
    if isinstance(value, str):
        value = value.replace(',', '.')
        try:
            return float(value)
        except ValueError:
            return None
    return value


def process_line(line):
    if line.startswith('APHUBDEV-'):
        parts = line.split()
        key = parts[0]
        time = to_float(parts[1])
        return key, time


def get_content_by_days(content):
    content_by_days = {}
    for day in re.split(r'\* ', content):
        day = day.strip()
        if not day:
            continue
        lines = day.splitlines()
        date = lines[0].strip()
        time_entries = []
        for line in lines[1:]:
            processed_line = process_line(line)
            if processed_line:
                time_entries.append(processed_line)
        content_by_days[date] = time_entries
    return content_by_days


def get_epics_with_stories(jira, story_keys):
    epics_with_stories = {}
    for story_key in story_keys:
        try:
            issue = jira.issue(story_key)
            parent_name = issue.fields.parent.fields.summary if issue.fields.parent else None
            parent_key = issue.fields.parent.key if issue.fields.parent else None
            if parent_key not in epics_with_stories:
                epics_with_stories[parent_key] = {
                    'name': parent_name,
                    'stories': []
                }
            epics_with_stories[parent_key]['stories'].append(story_key)
        except Exception as e:
            print(f"Error retrieving parent for {story_key}: {str(e)}")
    return epics_with_stories


def get_grouped_epics_by_day(content_by_days, epics_with_stories):
    epics_by_day = {}
    for date, stories_with_time in content_by_days.items():
        epics_by_day[date] = {}
        for story_key, time in stories_with_time:
            for epic_key, epic_data in epics_with_stories.items():
                if story_key in epic_data['stories']:
                    if epic_key not in epics_by_day[date]:
                        epics_by_day[date][epic_key] = {
                            'name': epic_data['name'],
                            'stories': [],
                            'total_time': 0.0
                        }
                    epics_by_day[date][epic_key]['stories'].append((story_key, time))
                    epics_by_day[date][epic_key]['total_time'] += time
    return epics_by_day


def print_formatted_output(epics_by_day):
    for date, epics in epics_by_day.items():
        print(date)
        for epic_key, epic_data in epics.items():
            print(f"  {epic_data['name']} [{epic_key}]:")
            print(f"    Total Time: {epic_data['total_time']}")
            print(f"    Stories:")
            for story_key, time in epic_data['stories']:
                print(f"      {story_key}: {time}")
        print("\n")
