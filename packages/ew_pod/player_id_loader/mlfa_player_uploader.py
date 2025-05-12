import os

import requests

game_year = os.environ.get('EW_GAME_YEAR')
api_url = os.environ.get('EW_API_URL')

endpoint = f'{api_url}/mlfad/player/for-year/{game_year}/bulk'

def upload_players(players):
    print(f'Uploading {len(players)} players to {endpoint}')
    response = requests.post(endpoint, json=players)

    if response.status_code == 200:
        print(f"{len(players)} players uploaded successfully.")
    else:
        print(f"Failed to upload players: {response.status_code} - {response.text}")

    return response.status_code