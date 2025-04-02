import requests
from typing import List
import json
import sys

def get_daily_game_info() -> List[dict]:
    """
    Retrieves today's game data from the NHL API and extracts useful 
    display data such as team names, score, and game state.
    """
    url = "https://api-web.nhle.com/v1/score/now"
    response = requests.get(url)
    if not response.ok:
        return None

    data = response.json()
    games = data['games']
    game_data = []
    for game in games:
        state = game['gameState']
        score = "0 - 0"
        if state in ["OFF", "LIVE", "FINAL"]:
            score = f"{game['awayTeam']['score']} - {game['homeTeam']['score']}"
        awayName = game['awayTeam']['abbrev']
        awayLogo = game['awayTeam']['logo']
        homeName = game['homeTeam']['abbrev']
        homeLogo = game['homeTeam']['logo']

        game_data.append({
            'awayLogoURL': awayLogo,
            'awayShortName': awayName,
            'homeLogoURL': homeLogo,
            'homeShortName': homeName,
            'score_string': score,
            'state_string': state
        })
    
    return game_data


if __name__ == "__main__":
    game_data = get_daily_game_info()
    if game_data is None:
        print("Error: network request failed")
        sys.exit(1)
    
    for game_info in game_data:
        obj = json.dumps(game_info, indent=4)
        print(obj)
