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

game_designer_s_path = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "bgg"
    / "game_designer"
)

game_designer_s_path.mkdir(
    parents=True,
    exist_ok=True
)

designer_s_path = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "bgg"
    / "designer"
)

designer_s_path.mkdir(
    parents=True,
    exist_ok=True
)

game_artist_s_path = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "bgg"
    / "game_artist"
)

game_artist_s_path.mkdir(
    parents=True,
    exist_ok=True
)

artist_s_path = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "bgg"
    / "artist"
)

artist_s_path.mkdir(
    parents=True,
    exist_ok=True
)

game_publi_s_path = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "bgg"
    / "game_publisher"
)

game_publi_s_path.mkdir(
    parents=True,
    exist_ok=True
)

publi_s_path = (
    PROJECT_ROOT
    / "data"
    / "silver"
    / "bgg"
    / "publisher"
)

publi_s_path.mkdir(
    parents=True,
    exist_ok=True
)

games_output = games_silver_path / "games.parquet"

game_categories_output = game_categories_silver_path / "game_categories.parquet"

categories_output = categories_silver_path / "categories.parquet"

game_mechanics_output = game_mechanics_s_path / "game_mechanics.parquet"

mechanics_output = mechanics_s_path / "mechanics.parquet"

game_designer_output = game_designer_s_path / "game_designer.parquet"

designer_output = designer_s_path / "designer.parquet"

game_artist_output = game_artist_s_path / "game_artist.parquet"

artist_output = artist_s_path / "artist.parquet"

game_publi_output = game_publi_s_path / "game_publi.parquet"

publi_output = publi_s_path / "publi.parquet"

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
designer = []
game_designer = []
artist = []
game_artist = []
publi = []
game_publi = []

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

                elif link_type == "boardgamedesigner":
                    designer_id = link.get("id")
                    designer_name = link.get("value")

                    if designer_id is None:
                        continue

                    designer.append({
                        "designer_id": int(designer_id),
                        "designer_name": designer_name,
                    })

                    game_designer.append({
                        "game_id": game_id,
                        "designer_id": int(designer_id),
                    })

                elif link_type == "boardgameartist":
                    artist_id = link.get("id")
                    artist_name = link.get("value")

                    if artist_id is None:
                        continue

                    artist.append({
                        "artist_id": int(artist_id),
                        "artist_name": artist_name,
                    })

                    game_artist.append({
                        "game_id": game_id,
                        "artist_id": int(artist_id),
                    })

                elif link_type == "boardgamepublisher":
                    publi_id = link.get("id")
                    publi_name = link.get("value")

                    if publi_id is None:
                        continue

                    publi.append({
                        "publi_id": int(publi_id),
                        "publi_name": publi_name,
                    })

                    game_publi.append({
                        "game_id": game_id,
                        "publi_id": int(publi_id),
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

df_designers = pd.DataFrame(designer)
df_designers = df_designers.drop_duplicates(
    subset=["designer_id"]
)

df_game_designers = pd.DataFrame(game_designer)
duplicate_relations_designers = df_game_designers.duplicated(
    subset=["game_id", "designer_id"]
).sum()

invalid_designer = ~df_game_designers[
    "designer_id"
].isin(df_designers["designer_id"])

df_artists = pd.DataFrame(artist)
df_artists = df_artists.drop_duplicates(
    subset=["artist_id"]
)

df_game_artist =  pd.DataFrame(game_artist)
duplicate_relations_artist = df_game_artist.duplicated(
    subset=["game_id", "artist_id"]
).sum()

invalid_artist = ~df_game_artist[
    "artist_id"
].isin(df_artists["artist_id"])

df_publishers = pd.DataFrame(publi)
df_publishers = df_publishers.drop_duplicates(
    subset=["publi_id"]
)

df_game_publishers = pd.DataFrame(game_publi)
duplicate_relations_publisher = df_game_publishers.duplicated(
    subset=["game_id", "publi_id"]
).sum()

invalid_publisher = ~df_game_publishers[
    "publi_id"
].isin(df_publishers["publi_id"])

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
def extract_relation(
        item,
        game_id,
        link_type, 
        entity_id_column,
        entity_name_column
    ):

    entities = []
    relations = []

    for link in item.findall("link"):

        current_link_type = link.get("type")

        if current_link_type == link_type:
            #print(link.get("id"), link.get("value"))
            entity_id = link.get("id")
            entity_name = link.get("value")

            if entity_id is None:
                continue

            entities.append({
                "entity_id_column": int(entity_id),
                "entity_name_column": entity_name,
                })
            
            relations.append({
                "game_id": game_id,
                "entity_id_column": int(entity_id),
                })
            
    return entities, relations 
    
new_categories, new_game_categories = extract_relation(
    item=item,
    game_id=game_id,
    link_type="boardgamecategory",
    entity_id_column="category_id",
    entity_name_column="category_name",
)

categories.extend(new_categories)
game_categories.extend(new_game_categories)

"""--------------------------"""

def validate_relation(
        relation_df,
        parent_df,
        relation_key,
        parent_key,
        relation_name
):
    invalid_rows = ~relation_df[relation_key].isin(parent_df[parent_key])
    invalid_count = invalid_rows.sum()
    logging.info(f"{relation_name} | inválidos: {invalid_count}")

    if invalid_count > 0:
        raise ValueError(
            f"Falha de integridade em {relation_name}: "
            f"{invalid_count} referências inválidas"
        )
    return invalid_count

validate_relation(
    relation_df=df_game_mechanics,
    parent_df=df_mechanics,
    relation_key="mechanic_id",
    parent_key="mechanic_id",
    relation_name="game_mechanics -> mechanics"
)

validate_relation(
    relation_df=df_game_mechanics,
    parent_df=df,
    relation_key="game_id",
    parent_key="id",
    relation_name="game_mechanics -> games"
)

validate_relation(
    relation_df=df_game_categories,
    parent_df=df_categories,
    relation_key="category_id",
    parent_key="category_id",
    relation_name="game_categories -> categories"
)

validate_relation(
    relation_df=df_game_categories,
    parent_df=df,
    relation_key="game_id",
    parent_key="id",
    relation_name="game_categories -> games"
)

validate_relation(
    relation_df=df_game_designers,
    parent_df=df_designers,
    relation_key="designer_id",
    parent_key="designer_id",
    relation_name="game_designers -> designer"
)

validate_relation(
    relation_df=df_game_designers,
    parent_df=df,
    relation_key="game_id",
    parent_key="id",
    relation_name="game_designers -> games"
)

validate_relation(
    relation_df=df_game_artist,
    parent_df=df_artists,
    relation_key="artist_id",
    parent_key="artist_id",
    relation_name="game_artists -> artists"
)

validate_relation(
    relation_df=df_game_artist,
    parent_df=df,
    relation_key="game_id",
    parent_key="id",
    relation_name="game_artists -> games"
)

validate_relation(
    relation_df=df_game_publishers,
    parent_df=df_publishers,
    relation_key="publi_id",
    parent_key="publi_id",
    relation_name="game_publishers -> publishers"
)

validate_relation(
    relation_df=df_game_publishers,
    parent_df=df,
    relation_key="game_id",
    parent_key="id",
    relation_name="game_publishers -> games"
)

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

df_designers.to_parquet(
    designer_output,
    index=False
)

df_game_designers.to_parquet(
    game_designer_output,
    index=False
)

df_artists.to_parquet(
    artist_output,
    index=False
)

df_game_artist.to_parquet(
    game_artist_output,
    index=False
)

df_publishers.to_parquet(
    publi_output,
    index=False
)

df_game_publishers.to_parquet(
    game_publi_output,
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
logging.info(
    f"Designers salvos: {len(df_designers)}"
)

logging.info(
    f"Relações jogo-designers salvas: {len(df_game_designers)}"
)

logging.info(
    f"Artistas salvos: {len(df_artists)}"
)

logging.info(
    f"Relações jogo-artistas salvas: {len(df_game_artist)}"
)

logging.info(
    f"Publishers salvas: {len(df_publishers)}"
)

logging.info(
    f"Relações jogo-publishers salvas: {len(df_game_publishers)}"
)
