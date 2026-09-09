import xml.etree.ElementTree as ET
import pandas as pd
import html
import logging
from pathlib import Path
from xml.etree.ElementTree import Element
from validate_bgg import validate_silver


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]

bronze_path = (
    PROJECT_ROOT
    / "data"
    / "bronze"
    / "bgg"
    / "thing"
)

games_silver_path = ( 
    PROJECT_ROOT
    / "data"
    / "silver"
    / "bgg"
    / "games"
)

games_silver_path.mkdir(
    parents=True,
    exist_ok=True
)

game_categories_silver_path = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "bgg"
    / "game_categories"
)

game_categories_silver_path.mkdir(
    parents=True,
    exist_ok=True
)

categories_silver_path = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "bgg"
    / "categories"
)

categories_silver_path.mkdir(
    parents=True,
    exist_ok=True
)

game_mechanics_s_path = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "bgg"
    / "game_mechanics"
)

game_mechanics_s_path.mkdir(
    parents=True,
    exist_ok=True
)

mechanics_s_path = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "bgg"
    / "mechanics"
)

mechanics_s_path.mkdir(
    parents=True,
    exist_ok=True
)

games_output = games_silver_path / "games.parquet"

game_categories_output = game_categories_silver_path / "game_categories.parquet"

categories_output = categories_silver_path / "categories.parquet"

game_mechanics_output = game_mechanics_s_path / "game_mechanics.parquet"

mechanics_output = mechanics_s_path / "mechanics.parquet"

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


def parse_game(item: Element) -> dict:

    game_id_raw = item.get("id")

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

games = []
categories = []
game_categories = []
mechanics = []
game_mechanics = []

raw_count = 0
parsed_count = 0
error_count = 0

for xml_file in bronze_path.glob("*.xml"):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    items = root.findall("item")

    raw_count += len(items)

    for item in items:
        try:
            game = parse_game(item)
            games.append(game)

            game_id = game["id"]

            for link in item.findall("link"):
                link_type = link.get("type")

                if link_type == "boardgamecategory":
                    #print(link.get("id"), link.get("value"))
                    category_id = link.get("id")
                    category_name = link.get("value")

                    if category_id is None:
                        continue

                    categories.append({
                        "category_id": int(category_id),
                        "category_name": category_name,
                        })
                    
                    game_categories.append({
                        "game_id": game_id,
                        "category_id": int(category_id),
                        })

                elif link_type == "boardgamemechanic":
                    mechanic_id = link.get("id")
                    mechanic_name = link.get("value")

                    if mechanic_id is None:
                        continue

                    mechanics.append({
                        "mechanic_id": int(mechanic_id),
                        "mechanic_name": mechanic_name,
                    })

                    game_mechanics.append({
                        "game_id": game_id,
                        "mechanic_id": int(mechanic_id),
                    })

            parsed_count += 1
        except Exception as e:
            error_count += 1

            logging.error(f"Erro processando game_id={item.get('id')}: {e}")

if raw_count != parsed_count + error_count:
    raise RuntimeError(
        "Inconsistênciaa entre registros lidos, processados com erro"
    )

df = pd.DataFrame(games)

df_categories = pd.DataFrame(categories)
df_categories = df_categories.drop_duplicates(
    subset=["category_id"]
)

df_game_categories = pd.DataFrame(game_categories)
duplicate_relations_categories = df_game_categories.duplicated(
    subset=["game_id", "category_id"]
).sum()

invalid_categories = ~df_game_categories[
    "category_id"
].isin(df_categories["category_id"])

invalid_games = ~df_game_categories[
    "game_id"
].isin(df["id"])

df_mechanics = pd.DataFrame(mechanics)
df_mechanics = df_mechanics.drop_duplicates(
    subset=["mechanic_id"]
)

df_game_mechanics = pd.DataFrame(game_mechanics)
duplicate_relations_mechanics = df_game_mechanics.duplicated(
    subset=["game_id", "mechanic_id"]
).sum()

invalid_mechanic = ~df_game_mechanics[
    "mechanic_id"
].isin(df_mechanics["mechanic_id"])

print(df_categories)
print(df_game_categories)
print(df_mechanics)
print(df_game_mechanics)

# print("Categorias:", len(df_categories))
# print(
#     "Categorias únicas:",
#     df_categories["category_id"].nunique()
# )
# print("Relações de categorias duplicadas:", duplicate_relations_categories)
# print("Categorias inexistentes:", invalid_categories.sum())
# print("Jogos inexistentes: ", invalid_games.sum())

results = validate_silver(df)
#print(results)

"""linha de testes abaixo"""
"""--------------------------"""

validation_results = results

logging.info(
    f"Validação concluída: {validation_results}"
)

duplicate_count = df["id"].duplicated().sum()

logging.info(f"IDs duplicados encontrados: {duplicate_count}")
logging.info(f"Jogos processados: {len(df)}")

df.to_parquet(
    games_output,
    index=False
)

df_categories.to_parquet(
    categories_output, 
    index=False
)

df_game_categories.to_parquet(
    game_categories_output,
    index=False
)

df_mechanics.to_parquet(
    mechanics_output,
    index=False
)

df_game_mechanics.to_parquet(
    game_mechanics_output,
    index=False
)

logging.info(
    f"Processamento concluído | "
    f"raw={raw_count} | "
    f"parsed={parsed_count} | "
    f"errors={error_count}"
)
logging.info(f"Games salvos em: {games_output}")

logging.info(
    f"Categorias salvas: {len(df_categories)}"
)

logging.info(
    f"Relações jogo-categoria salvas: {len(df_game_categories)}"
)

logging.info(
    f"Mecanicas salvas: {len(df_mechanics)}"
)

logging.info(
    f"Relações jogo-mecanicas salvas: {len(df_game_mechanics)}"
)

