from clockify_api_client.client import ClockifyAPIClient
import requests

# SETUP
API_KEY = 'MjFlY2M3OWUtMDY2MC00NDM3LThmNmYtMTU3NjAwYTFlYzkz'  # api key from 'https://app.clockify.me/user/settings'
API_URL = 'api.clockify.me/v1'
base_url = 'https://api.clockify.me/api/v1'
headers = {'content-type': 'application/json', 'X-Api-Key': API_KEY}  # requied headres for future request

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
# Print out all the etries/tasks from oldest to most recent
[print(time_entry['description']) for time_entry in time_entries[::-1]]