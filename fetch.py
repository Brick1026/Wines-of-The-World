# Retrieves data from API

import threading
import httpx
import json
import random
from concurrent.futures import ThreadPoolExecutor

_WRITE_LOCK = threading.Lock()

# how large of a set of wines do we want
MASTER_DATA_SIZE = 10000

wines = []

def fetch():
    with httpx.Client(timeout=15.0) as client:
        response = client.get("https://vinofyi.com/api/v1/wines/")
        response.raise_for_status()
        catalog = response.json()["results"]

        with ThreadPoolExecutor(max_workers=4) as pool:
            for i in range(0,MASTER_DATA_SIZE + 1):
                pool.submit(query_thread, catalog)

    with open('Data\\master_wine_data.json', "w") as file:
        json.dump(wines, file, indent=4)
    
# Thread to query database and then write it's result into array
def query_thread(catalog):
    wine = random.choice(catalog)
    wine = {
        "wine": wine.get("name"),
        "type": wine.get("wine_type"),
        "acidity": wine.get("acidity"),
        "abv": wine.get("abv"),
        "country_name": wine.get("country_name"),
        "body": wine.get("body"),
        "winery_name": wine.get("winery_name"),
    }
    with _WRITE_LOCK:
        wines.append(wine)
    