import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import time

load_dotenv()

ACCESS_TOKEN = os.getenv("BGG_token")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

url = "https://boardgamegeek.com/xmlapi2/thing"

game_ids = [1, 2, 3, 4, 5, 6, 7]


import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def chunk_list(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]
    


def download_bgg_data(url: str, headers: dict, params:dict, batch_number:int) -> str:
    
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
    
    output_path = f'data/bronze/bgg/thing/batch_{batch_number:04d}_{datetime.now().strftime("%Y-%m-%d")}.xml'
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding="utf-8") as f:
        f.write(data)

    logging.info(f"Arquivo salvo em {output_path}")
    
    return data
    
for batch_number,batch in enumerate(
    chunk_list(game_ids, 3), start=1
    ):
    ids_param = ",".join(map(str,batch))
    params = {
    "id": ids_param,
    "stats": 1
    }
    logging.info(f"Processando batch -> {batch} - IDs: {ids_param}")

    download_bgg_data(
    url=url,
    headers=headers,
    params=params,
    batch_number=batch_number,
    ) 
    
    time.sleep(5)


