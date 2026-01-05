from ba_parser import load_players_from_ba
from ba_uploader import upload_players


def main():
    try:
        players = load_players_from_ba()

        upload_players(players)

        return {"statusCode": 200, "body": {"players": players}}

    except Exception as e:
        return {"statusCode": 500, "body": {"message": f"An error occurred: {e}"}}
