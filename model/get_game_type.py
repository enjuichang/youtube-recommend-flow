import requests
import json
from pprint import pprint
    
def getSteamGenre(game_name):
    game_obj = searchSteam(game_name)
    cats = getCategory(game_obj)
    return [cat['description'] for cat in cats]
    
def searchSteam(game_name):
    response = requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/")

    # change the JSON string into a JSON object
    all_games_base = json.loads(response.content)
    all_games = all_games_base["applist"]["apps"]

    # Storage
    game_list = []

    # print the keys and values
    for game_obj in all_games:
        # Exact query match (could do regrex in the future)
        if game_name.lower() in game_obj['name'].lower():
            # if complete match
            if game_name.lower() == game_obj['name'].lower():
                return game_obj
            # If name included
            else:
                game_list.append(game_obj)

    if not game_list:
        raise ValueError("Game not in Steam Database")
    return game_list

def getCategory(game_obj):
    # If there is a complete match
    try:
        try:
            game_id = game_obj['appid']
            response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={game_id}")
            contents = json.loads(response.content)
            return contents[f"{game_id}"]['data']['genres']
        # If data not found
        except:
            raise ValueError("Game info not found")
    # If there is a list
    except:
        try:
            # Right now just get the first
            game_id = game_obj[0]['appid']
            response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={game_id}")
            contents = json.loads(response.content)
            return contents[f"{game_id}"]['data']['genres']
        # If data not found
        except:
            raise ValueError("Game info not found")

if __name__ == "__main__":
    cats = getSteamGenre('Minecraft')
    print(cats)