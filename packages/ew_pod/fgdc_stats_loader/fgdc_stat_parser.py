import os
import time
from dataclasses import dataclass
from datetime import datetime

import requests
from bs4 import BeautifulSoup

pitcher_stat = 'TBF'
hitter_stat = 'PA'

game_year = os.environ.get('EW_GAME_YEAR')

@dataclass
class Player:
    def __init__(self, year: str, fg_id:str, sa_id:str, name: str, team: str, fg_team: str, ba_position: str, fg_position: str, url: str):
        self.year = year
        self.fg_id = fg_id
        self.sa_id = sa_id
        self.name = name
        self.team = team
        self.fg_team = fg_team
        self.ba_position = ba_position
        self.fg_position = fg_position
        self.url = url

    @staticmethod
    def from_json(json: dict):
        return Player(
            year=json.get('year'),
            fg_id=json.get('fgId'),
            sa_id=json.get('saId'),
            name=json.get('name'),
            team=json.get('team'),
            fg_team=json.get('fgTeam'),
            ba_position=json.get('baPosition'),
            fg_position=json.get('fgPosition'),
            url=json.get('url')
        )

    def __str__(self):
        return str(self.__dict__)

def get_player_page(player: Player):
    player_page_url = f'https://www.fangraphs.com/{player.url}'
    page = requests.get(player_page_url)
    if not page.ok:
        print(f"Fangraphs page request is not OK? {page.status_code}")
    soup = BeautifulSoup(page.text, features='lxml')
    return soup

def get_player_stats(player: Player) -> dict:
    soup_page = get_player_page(player)

    standard_table = soup_page.select_one('div#standard table')
    mlb_rows = standard_table.select('tr.row-mlb-season')
    projection_rows = standard_table.select('tr.row-projection')

    stats = {}

    for row in mlb_rows:
        season_td = row.select_one('td[data-stat="Season"]')
        if season_td is not None:
            season = season_td.text
            if season == game_year:
                stat_id = pitcher_stat if player.fg_position == 'P' else hitter_stat
                stat_td = row.select_one(f'td[data-stat="{stat_id}"]')
                numeric_stat = int(stat_td.text) if stat_td.text.isdigit() else 0
                stats['actualStat'] = numeric_stat
                break

    for row in projection_rows:
        team_td = row.select_one('td[data-stat="Team"] a')
        if team_td is not None:
            team = team_td.text
            if team == 'FGDC':
                stat_id = pitcher_stat if player.fg_position == 'P' else hitter_stat
                stat_td = row.select_one(f'td[data-stat="{stat_id}"]')
                numeric_stat = int(stat_td.text) if stat_td.text.isdigit() else 0
                stats['projectedStat'] = numeric_stat
                break

    if not stats:
        print(f"Could not find FGDC stats for {player.name}")
    return stats

def load_mlfa_stats(players):
    player_results = []

    for player_json in players:
        player: Player = Player.from_json(player_json)
        try:
            stats = get_player_stats(player)
            print(f"{player.name} => Stat={stats}")
            player_results.append({
                "player": player.name,
                "playerId": player.fg_id,
                "projectedStat": stats.get('projectedStat', 0),
                "actualStat": stats.get('actualStat', 0),
                "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            })
            time.sleep(0.1)
        except Exception as e:
            print(f"Error with {player.name}: {e}")

    return player_results