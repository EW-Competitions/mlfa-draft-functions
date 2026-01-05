import re

from team_mapping import mlb_teams

ba_mlfa_players_file_name = "ba-mlfa-players.txt"

# Example: RHP Bryse Wilson (AAA)
player_regex = r"^(?P<position>[A-Z1-3]{1,3}) (?P<name>.+) \((?P<level>.+)\)$"


def load_players_from_ba():
    team_players_dict: dict[str, list] = {}
    with open(ba_mlfa_players_file_name, "r") as ba_player_file:
        players_list = ba_player_file.read()

        team = None
        for line in players_list.split("\n"):
            if line.strip() == "":
                team = None
            elif team is None:
                team = line
                team_players_dict[team] = []
            else:
                pr = re.search(player_regex, line)
                player = pr.groupdict()
                team_players_dict[team].append(player)

    players = []

    for team, team_players in team_players_dict.items():
        for player in team_players:
            player_team = next(
                (mlb_team for mlb_team in mlb_teams if mlb_teams[mlb_team] == team),
                None,
            )
            players.append(
                {
                    "player": player["name"],
                    "position": player["position"],
                    "level": player["level"],
                    "team": player_team,
                }
            )

    return players
