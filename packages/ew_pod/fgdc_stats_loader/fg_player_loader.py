import os

import requests

game_year = os.environ.get('EW_GAME_YEAR')
api_url = os.environ.get('EW_API_URL')

endpoint = f'{api_url}/mlfad/player/for-year/{game_year}/'

def load_fg_players():
    print(f'Loading players from {endpoint}')
    response = requests.get(endpoint)

    if response.status_code == 200:
        players = response.json()
        print(f"Loaded {len(players)} players.")
        return players
    else:
        print(f"Failed to load players: {response.status_code} - {response.text}")
        return []