import re

import requests
from bs4 import BeautifulSoup
from team_mapping import mlb_teams

mlfa_url = "https://www.baseballamerica.com/stories/minor-league-free-agents-2024/"

# Example: RHP Bryse Wilson (AAA)
player_regex = r'^(?P<position>[A-Z1-3]{1,3}) (?P<name>.+) \((?P<level>.+)\)$'

def load_players_from_ba():
    page = requests.get(mlfa_url)

    soup = BeautifulSoup(page.text, features='lxml')

    main = soup.select_one('div.page-layout__main')

    paragraphs = main.select('p')

    teams = {}

    for paragraph in paragraphs:
        p_html = str(paragraph)
        if '<strong>' in p_html:
            html = (
                # Clear out any formatting tags
                str(paragraph)
                .replace("<p>", "")
                .replace("</p>", "")
                .replace("<br/></strong>", "</strong><br/>")
                .replace("<br></strong>", "</strong><br/>")
                .replace("<br/>", "\n")
            )

            current_team = ''

            for line in html.split("\n"):
                if '<strong>' in line:
                    current_team = line.replace('<strong>', '').replace('</strong>', '')
                    teams[current_team] = []
                elif line.strip() != '':
                    pr = re.search(player_regex, line)
                    player = pr.groupdict()
                    teams[current_team].append(player)

    players = []

    for team, team_players in teams.items():
        for player in team_players:
            player_team = next((
                mlb_team
                for mlb_team in mlb_teams
                if mlb_teams[mlb_team] == team
            ), None)
            players.append({
                'player': player['name'],
                'position': player['position'],
                'level': player['level'],
                'team': player_team,
            })

    return players