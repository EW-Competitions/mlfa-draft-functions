import os

import requests

game_year = os.environ.get('EW_GAME_YEAR')
api_url = os.environ.get('EW_API_URL')

endpoint = f'{api_url}/mlfad/ba-player/for-year/{game_year}/'

def load_ba_players():
    response = requests.get(endpoint)

    if response.status_code == 200:
        players = response.json()
        print(f"Loaded {len(players)} BA players.")
        return players
    else:
        print(f"Failed to load BA players: {response.status_code} - {response.text}")
        return []
