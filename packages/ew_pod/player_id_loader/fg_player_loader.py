import os
import time

import requests
from unidecode import unidecode

from bg_to_fg_player_mapping import (
    ba_to_fg_position_mapping,
    ba_to_fg_name_mapping,
    ba_to_fg_birthdate_mapping,
)
from team_mapping import fg_mlb_team_to_team_id

url = os.environ.get("FG_SEARCH_URL")


def get_request_body(query_string):
    return {
        "query": query_string,
        "page": {"size": 20, "current": 1},
        "search_fields": {"name": {}},
        "result_fields": {
            "id": {"raw": {}},
            "name": {"raw": {}},
            "birthdate": {"raw": {}},
            "team": {"raw": {}},
            "url": {"raw": {}},
            "position": {"raw": {}},
        },
        "filters": {"any": [{"level": ["major", "minor"]}]},
    }


def map_position(position, player_name):
    if position == "LHP" or position == "RHP":
        return "P"
    if player_name in ba_to_fg_position_mapping:
        return ba_to_fg_position_mapping[player_name]
    return position


def map_fangraphs_teams(raw_team: str):
    return fg_mlb_team_to_team_id.get(raw_team, raw_team)


def get_player_with_id(headers, player_name, player_team, player_position):
    try:
        player_name = (
            ba_to_fg_name_mapping[player_name]
            if player_name in ba_to_fg_name_mapping
            else player_name
        )
        body = get_request_body(unidecode(player_name))

        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            data = response.json()

            results = data["results"]

            filtered_players = [
                p
                for p in results
                if unidecode(p["name"]["raw"]) == unidecode(player_name)
            ]

            if len(filtered_players) > 1:
                mapped_position = map_position(player_position, player_name)
                filtered_players = [
                    p
                    for p in filtered_players
                    if p["position"]["raw"] == mapped_position
                ]

            if len(filtered_players) > 1:
                birthdate = (
                    ba_to_fg_birthdate_mapping[player_name]
                    if player_name in ba_to_fg_birthdate_mapping
                    else None
                )
                if birthdate:
                    filtered_players = [
                        p
                        for p in filtered_players
                        if p["birthdate"]["raw"].startswith(birthdate)
                    ]

            if len(filtered_players) != 1:
                print(f"Error: Found {len(filtered_players)} players for {player_name}")
                return None

            searched_player = filtered_players[0]
            player_id = searched_player["id"]["raw"]

            return {
                "year": os.environ.get("EW_GAME_YEAR"),
                "fgId": player_id,
                "saId": player_id if player_id.startswith("sa") else None,
                "name": searched_player["name"]["raw"].replace("  ", " "),
                "baTeam": player_team,
                "fgTeam": map_fangraphs_teams(searched_player["team"]["raw"]),
                "baPosition": player_position,
                "fgPosition": searched_player["position"]["raw"],
                "url": searched_player["url"]["raw"],
            }
        else:
            print(f"Error searching for {player_name}: {response.json()}")
            return None
    except Exception as e:
        print(f"Error searching for {player_name}: {e}")
        return None


def load_players_with_ids(players):
    print("this will load players with their FG IDs")

    token = os.environ.get("FG_SEARCH_TOKEN")

    headers = {"Authorization": token, "Content-Type": "application/json"}

    loaded_players = []

    for player in players:
        player_with_id = get_player_with_id(
            headers, player["player"], player["team"], player["position"]
        )
        if player_with_id:
            loaded_players.append(player_with_id)
        time.sleep(0.5)

    return loaded_players
