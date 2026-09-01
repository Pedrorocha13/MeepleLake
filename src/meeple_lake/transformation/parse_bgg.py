import xml.etree.ElementTree as ET
import pandas as pd
import html

from pathlib import Path
from xml.etree.ElementTree import Element


PROJECT_ROOT = Path(__file__).resolve().parents[3]

bronze_path = (
    PROJECT_ROOT
    / "data"
    / "bronze"
    / "bgg"
    / "thing"
)


def get_int(element: Element, tag: str, default: int | None = None) -> int | None:

    child = element.find(tag)

    if child is None:
        return default

    value = child.get("value")

    if value is None:
        return default

    try:
        return int(value)
    except ValueError:
        return default


def get_float(element: Element, tag: str, default: float | None = None) -> float | None:

    child = element.find(tag)

    if child is None:
        return default

    value = child.get("value")

    if value is None:
        return default

    try:
        return float(value)
    except ValueError:
        return default


def parse_game(xml_path: Path) -> dict:

    tree = ET.parse(xml_path)
    root = tree.getroot()

    item = root.find("item")

    if item is None:
        raise ValueError(
            f"XML {xml_path.name} não contém elemento <item>"
        )

    game_id_raw = item.get("id")

    if game_id_raw is None:
        raise ValueError(
            f"XML {xml_path.name} não contém id do jogo"
        )

    game_id = int(game_id_raw)

    primary_name = item.find(
        "name[@type='primary']"
    )

    if primary_name is not None:
        game_name = primary_name.get("value")
    else:
        game_name = None


    year_publi = get_int(item, "yearpublished")

    min_player = get_int(item, "minplayers")

    max_player = get_int(item, "maxplayers")

    playing_time = get_int(item, "playingtime")

    min_play_time = get_int(item, "minplaytime")

    max_play_time = get_int(item, "maxplaytime")

    min_age = get_int(item, "minage")

    statistics = item.find("statistics")

    user_rated = None
    average_rating = None
    bayes_average = None
    overall_ranking = None
    owned = None
    for_trading = None
    pp_wanting = None
    pp_wishing = None
    avrg_weight = None
    num_comments = None
    num_weights = None

    if statistics is not None:

        ratings = statistics.find("ratings")

        if ratings is not None:

            user_rated = get_int(ratings, "usersrated")

            average_rating = get_float(ratings, "average")

            bayes_average = get_float(ratings,"bayesaverage")

            owned = get_int(ratings,"owned")

            for_trading = get_int(ratings,"trading")

            pp_wanting = get_int(ratings,"wanting")

            pp_wishing = get_int(ratings,"wishing")

            avrg_weight = get_float(ratings,"averageweight")

            num_comments = get_int(ratings,"numcomments")

            num_weights = get_int(ratings,"numweights")

            # Ranking
            ranks = ratings.find("ranks")

            if ranks is not None:

                rank = ranks.find(
                    "rank[@name='boardgame']"
    )

                if rank is not None:

                    rank_value = rank.get("value")

                    if (
                        rank_value is not None
                        and rank_value.isdigit()
        ):
                        overall_ranking = int(
                            rank_value
            )


    description_element = item.find("description")

    if (
        description_element is not None
        and description_element.text
    ):

        description = html.unescape(description_element.text)

        description = " ".join(
            description.split()
        )

    else:
        description = None

 
    return {
        "id": game_id,
        "name": game_name,
        "year": year_publi,
        "min_player": min_player,
        "max_player": max_player,
        "playing_time": playing_time,
        "min_play_time": min_play_time,
        "max_play_time": max_play_time,
        "min_age": min_age,
        "user_rated": user_rated,
        "average_rating": average_rating,
        "bayes_average": bayes_average,
        "ranking": overall_ranking,
        "owned": owned,
        "for_trading": for_trading,
        "wanting": pp_wanting,
        "wishing": pp_wishing,
        "average_weight": avrg_weight,
        "num_comments": num_comments,
        "num_weights": num_weights,
        "description": description,
    }



