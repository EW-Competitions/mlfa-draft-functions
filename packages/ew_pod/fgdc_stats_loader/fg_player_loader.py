
import json

file_name = 'fg_player_id_do.json'

def load_fg_players():
    """
    This will eventually load players from a DB.
    For now, it comes from a JSON file.
    """
    return json.load(open(file_name, "r", encoding="utf-8"))['players']