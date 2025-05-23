from ba_player_loader import load_ba_players
from fg_player_loader import load_players_with_ids
from mlfa_player_uploader import upload_players


def main(args):
    ba_players = load_ba_players()

    print(f'Getting FG IDs for {len(ba_players)} players')

    players_with_ids = load_players_with_ids(ba_players)

    upload_players(players_with_ids)

    return {
        'statusCode': 200,
        'body': {
            'players': players_with_ids,
        }
    }