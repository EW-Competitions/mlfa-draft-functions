from fg_player_loader import load_fg_players
from fg_player_uploader import upload_results
from fgdc_stat_parser import load_mlfa_stats


def main():
    fg_players = load_fg_players()

    print(f'Getting current stat totals for {len(fg_players)} players')

    players_with_stats = load_mlfa_stats(fg_players)

    upload_results(players_with_stats)

    return {
        'statusCode': 200,
        'body': {
            'players': players_with_stats,
        }
    }