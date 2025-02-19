import json


def load_ba_players(args):
    # this will later get players from the database
    # for now, it'll use the players sent into the API
    #return args["players"] if "players" in args else []

    # load from the JSON file mlfa-players.json
    with open('mlfa-players.json', 'r') as file:
        return json.load(file)



