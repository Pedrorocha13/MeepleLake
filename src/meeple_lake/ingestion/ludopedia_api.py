import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("LUDOPEDIA_ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

url = "https://ludopedia.com.br/api/v1/jogos"

params = {
    "page": 1,
    "rows": 20
}

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_ludopedia_data(url: str, headers: dict, params:dict) -> dict:
    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        logging.warning("Dados nulos!")
        return[]
    
    output_path = 'data/boardgames.json'
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
    )

    logging.info(f"Arquivo salvo em {output_path}")

    return data

download_ludopedia_data(
    url=url,
    headers=headers,
    params=params
    )
