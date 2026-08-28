import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

ACCESS_TOKEN = os.getenv("BGG_token")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

url = "https://boardgamegeek.com/xmlapi2/thing"

params = {
    "id": "174431",
    "stats": 1
}

game_id = params["id"]

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_bgg_data(url: str, headers: dict, params:dict) -> str:
    response = requests.get(
        url=url,
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.text

    if not data:
        logging.warning("Dados nulos!")
        return ""
    
    output_path = f'data/bronze/bgg/thing/game_{game_id}_{datetime.now().strftime("%Y-%m-%d")}.xml'
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding="utf-8") as f:
        f.write(data)

    logging.info(f"Arquivo salvo em {output_path}")

    return data

download_bgg_data(
    url=url,
    headers=headers,
    params=params
    )
