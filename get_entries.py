from clockify_api_client.client import ClockifyAPIClient
import requests
import time
from datetime import datetime, timedelta


# SETUP
API_KEY = 'MjFlY2M3OWUtMDY2MC00NDM3LThmNmYtMTU3NjAwYTFlYzkz'  # api key from 'https://app.clockify.me/user/settings'
API_URL = 'api.clockify.me/v1'
base_url = 'https://api.clockify.me/api/v1'
headers = {'content-type': 'application/json', 'X-Api-Key': API_KEY}  # requied headres for future requests

# get workspace id
client = ClockifyAPIClient().build(API_KEY, API_URL)
workspaces = client.workspaces.get_workspaces()  # Returns list of workspaces.
workspace_id = workspaces[0]['id']

# get user and project id
url_for_project_id = base_url + f'/workspaces/{workspace_id}/projects'
response = requests.get(url_for_project_id, headers=headers)
user_id = response.json()[0]['memberships'][0]['userId']
project_id = response.json()[0]['id']


# get all time entries for our project
url_for_time_entries = base_url + f'/workspaces/{workspace_id}/user/{user_id}/time-entries'
response = requests.get(url_for_time_entries, headers=headers)
time_entries = response.json()
time_entries = time_entries[::-1]  # change the order of entries to: from oldest to most recent
total_time_spent = timedelta()
all_dates = dict()

for index, time_entry in enumerate(time_entries, start=1):
    # calculate the duration
    entry_start = datetime.strptime(time_entry['timeInterval']['start'], '%Y-%m-%dT%H:%M:%SZ')
    entry_end = datetime.strptime(time_entry['timeInterval']['end'], '%Y-%m-%dT%H:%M:%SZ')
    entry_duration = entry_end - entry_start
    total_time_spent += entry_duration
    # add new date and duration or increase the duration for existing date 
    entry_date = entry_start.strftime('%Y-%m-%d')
    if entry_date in all_dates:
        all_dates[entry_date] += entry_duration
    else:
        all_dates[entry_date] = entry_duration
    # OUTPUT
    print("###############################")
    print(f'Time entry #{index} - {time_entry["description"]}')  # Print out all the entries/tasks
    print(f'Duration: {entry_duration}')
    print("###############################\n")

print(f'Total time spent: {total_time_spent}\n')

print('Time spent by dates:')
[print(f'{date} - {all_dates[date]}') for date in all_dates]  # Print out all dates and duration of each