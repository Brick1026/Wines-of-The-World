# Retrieves data from API

import threading
import httpx
import json
import random
from concurrent.futures import ThreadPoolExecutor

_WRITE_LOCK = threading.Lock()

# how large of a set of wines do we want
MASTER_DATA_SIZE = 10000

GRAPE_TYPES = {
    "cabernet franc",
    "cabernet sauvignon",
    "chardonnay",
    "gamay",
    "gewurztraminer",
    "grenache",
    "malbec",
    "merlot",
    "mourvedre",
    "petite sirah",
    "pinot grigio",
    "pinot gris",
    "pinot noir",
    "riesling",
    "sangiovese",
    "sauvignon blanc",
    "semillon",
    "shiraz",
    "syrah",
    "tempranillo",
    "viognier",
    "zinfandel",
}

wines = []

def fetch():
    with httpx.Client(timeout=15.0) as client:
        # get list of wines (our catalog)
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
    # randomly select a wine from catalog
    wine = random.choice(catalog)
    name = wine.get("name")
    name_lower = str(name or "").casefold()
    wine = {
        "wine": name,
        "grapes": sorted(grape for grape in GRAPE_TYPES if grape in name_lower),
        "type": wine.get("wine_type"),
        "acidity": wine.get("acidity"),
        "abv": wine.get("abv"),
        "country_name": wine.get("country_name"),
        "body": wine.get("body"),
        "winery_name": wine.get("winery_name"),
        "region_name": wine.get("region_name")
    }
    with _WRITE_LOCK:
        wines.append(wine)
    