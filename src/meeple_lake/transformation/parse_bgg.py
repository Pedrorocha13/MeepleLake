import xml.etree.ElementTree as ET
import pandas as pd
import html
from pathlib import Path

bronze_path = Path(
    "/home/prjesus/projects/MeepleLake/data/bronze/bgg/thing"
)

def parse_game(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    item = root.find("item")
    game_id = int(item.get("id"))
    primary_name = item.find("name[@type='primary']")
    game_name = str(primary_name.get('value'))
    year_publi = int(item.find('yearpublished').get('value'))
    min_player = int(item.find("minplayers").get('value'))
    max_player = int(item.find("maxplayers").get('value'))
    playing_time = int(item.find("playingtime").get('value'))
    min_play_time = int(item.find("minplaytime").get('value'))
    max_play_time = int(item.find("maxplaytime").get('value'))
    min_age = int(item.find("minage").get('value'))
    statistics = item.find("statistics")
    ratings = statistics.find("ratings")
    user_rated = int(ratings.find("usersrated").get("value"))
    average_rating = float(ratings.find("average").get("value"))
    bayes_average = float(ratings.find("bayesaverage").get("value"))
    ranks = ratings.find("ranks").find("rank[@name='boardgame']")
    overall_ranking = int(ranks.get("value"))
    owned = int(ratings.find("owned").get("value"))
    for_trading = int(ratings.find("trading").get("value"))
    pp_wanting = int(ratings.find("wanting").get("value"))
    pp_wishing = int(ratings.find("wishing").get("value"))
    avrg_weight = float(ratings.find("averageweight").get("value"))
    num_comments = int(ratings.find("numcomments").get("value"))
    num_weights = int(ratings.find("numweights").get("value"))
    description_element = item.find("description")
    if description_element is not None and description_element.text:
        description = html.unescape(str(description_element.text))
        description = " ".join(description.split())
    else:
        description = None


    data_dict = {
        "id": game_id,
        "name": game_name,
        "year": year_publi,
        "min_player": min_player,
        "max_player": max_player,
        "min_playtime": min_play_time,
        "max_playtime": max_play_time,
        "playing_time": playing_time,
        "min_age": min_age,

        "rating": average_rating,
        "bayes_rating": bayes_average,
        "ranking": overall_ranking,
        "complexity": avrg_weight,
        "num_weights": num_weights,

        "user_rated": user_rated,
        "owners": owned,
        "to_trade": for_trading,
        "wanting": pp_wanting,
        "wishing": pp_wishing,
        "num_comments": num_comments,

        "description": description
    }
    return data_dict

games = []

for xml_file in bronze_path.glob("*.xml"):
    game = parse_game(xml_file)
    games.append(game)

df = pd.DataFrame(games)

print(df)
print(df.dtypes)