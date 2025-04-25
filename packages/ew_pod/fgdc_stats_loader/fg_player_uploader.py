import os

import requests

api_url = os.environ.get('EW_API_URL')

endpoint = f'{api_url}/mlfad/stats'

def upload_results(players_with_stats):
    response = requests.post(endpoint, json=players_with_stats)

    if response.status_code == 200:
        print(f"{len(players_with_stats)} players w/ stats uploaded successfully.")
    else:
        print(f"Failed to upload players w/ stats: {response.status_code} - {response.text}")

    return response.status_code