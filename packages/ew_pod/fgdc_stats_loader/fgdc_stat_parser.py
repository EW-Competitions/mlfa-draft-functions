import time
from dataclasses import dataclass
from datetime import datetime

import requests
from bs4 import BeautifulSoup

pitcher_stat = 'TBF'
hitter_stat = 'PA'

@dataclass
class Player:
    def __init__(self, id: str, name: str, team: str, fg_team: str, ba_position: str, position: str, url: str):
        self.id = id
        self.name = name
        self.team = team
        self.fg_team = fg_team
        self.ba_position = ba_position
        self.position = position
        self.url = url

    def __str__(self):
        return str(self.__dict__)

def get_player_page(player: Player):
    player_page_url = f'https://www.fangraphs.com/{player.url}'
    page = requests.get(player_page_url)
    if not page.ok:
        print(f"Not OK? {page.status_code}")
    soup = BeautifulSoup(page.text, features='lxml')
    return soup

def get_player_stats(player: Player) -> int:
    soup_page = get_player_page(player)

    standard_table = soup_page.select_one('div#standard table')
    projection_rows = standard_table.select('tr.row-projection')

    for row in projection_rows:
        team_td = row.select_one('td[data-stat="Team"] a')
        if team_td is not None:
            team = team_td.text
            if team == 'FGDC':
                stat_id = pitcher_stat if player.position == 'P' else hitter_stat
                stat_td = row.select_one(f'td[data-stat="{stat_id}"]')
                numeric_stat = int(stat_td.text) if stat_td.text.isdigit() else 0
                return numeric_stat

    print(f"Could not find FGDC for {player.name}")
    return 0

def load_mlfa_stats(players):
    player_results = []

    for player_json in players:
        player: Player = Player(**player_json)
        try:
            stats = get_player_stats(player)
            print(f"{player.name} => Stat={stats}")
            player_results.append({
                "player": player.name,
                "playerId": player.id,
                "playerUrl": player.url,
                "stat": stats,
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            })
            time.sleep(0.1)
        except Exception as e:
            print(f"Error with {player.name}: {e}")

    return player_results