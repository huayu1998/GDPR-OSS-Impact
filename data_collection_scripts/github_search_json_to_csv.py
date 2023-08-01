import json
import csv
import requests
from datetime import datetime

def parse(text):
    try:
        return json.loads(text)
    except ValueError as e:
        print('invalid json: %s' % e)
        return None # or: raise

x = requests.get('https://api.github.com/search/issues?q=gdpr+is:pull-request&per_page=100', headers={"Accept": "application/vnd.github+json", "Authorization": "Replace your authentication here"}, stream=True, timeout=60)

removed_bad_characters = x.content.decode('utf-8', 'ignore')
encoded_again = removed_bad_characters.encode("utf-8")
data = parse(encoded_again)
with open("py_request_pr.text", "w") as f:
    f.write(str(encoded_again))

data_file = open('data_file.csv', 'w')

csv_writer = csv.writer(data_file)

count = 0

fields = ["url", "title", "comments", "created_at", "updated_at", "active_time", "closed_at", "commits", "additions", "deletions", "changed_files"]

for issue in data["items"]:
    if count == 0:
        csv_writer.writerow(fields)
        count += 1
    row = []
    for field in fields:
        if field == "active_time":
            created_at = row[3]
            # created_datetime = datetime.fromisoformat(created_at)
            created_datetime = datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
            updated_at = row[4]
            # updated_datetime = datetime.fromisoformat(updated_at)
            updated_datetime = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%SZ')
            active_datetime = updated_datetime - created_datetime
            row.append(active_datetime.total_seconds())
        elif field == "commits":
            pr = issue.get("pull_request")
            pr_url = pr["url"]
            pr_response = requests.get(pr_url, headers={"Accept": "application/vnd.github+json", "Authorization": "Replace your authentication here"})
            pr_data = parse(pr_response.content)
            commits = pr_data.get("commits")
            additions = pr_data.get("additions")
            deletions = pr_data.get("deletions")
            changed_files = pr_data.get("changed_files")
            row.append(commits)
            row.append(additions)
            row.append(deletions)
            row.append(changed_files)
        elif field == "additions" or field == "deletions" or field == "changed_files":
            continue
        else:
            row.append(issue.get(field))
    try:
        csv_writer.writerow(row)
    except UnicodeEncodeError as e:
        csv_writer.writerow([])
    

data_file.close()