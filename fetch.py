# Retrieves data from API

import threading
import httpx
import json
import re
import random
from concurrent.futures import ThreadPoolExecutor

# list of all distinct grapes found during fetch with an assigned value
query_grapes = {}

# list of all entries seen
seen_entries = {}

# next distinct grape id
grape_id = 1

# list of all wines recorded during fetch
wines = []


_WRITE_LOCK = threading.Lock()

# Number of pages to build catalog to sample from
# each page is roughly 50 wines
PAGES = 20
# Number of random samples
MASTER_DATA_SIZE = 300


GRAPE_TYPES = {
    "aglianico",
    "albarino",
    "albariño",
    "alicante bouschet",
    "arneis",
    "assyrtiko",
    "barbera",
    "bobal",
    "bonarda",
    "brachetto",
    "cabernet franc",
    "cabernet sauvignon",
    "carmenere",
    "carignan",
    "chardonnay",
    "chenin blanc",
    "cinsault",
    "cortese",
    "corvina",
    "dolcetto",
    "dornfelder",
    "fiano",
    "frappato",
    "gamay",
    "garganega",
    "glera",
    "gewurztraminer",
    "grenache",
    "gruner veltliner",
    "grüner veltliner",
    "mencia",
    "mencía",
    "montepulciano",
    "malbec",
    "malvasia",
    "merlot",
    "mourvedre",
    "muller-thurgau",
    "müller-thurgau",
    "muscat",
    "nebbiolo",
    "negroamaro",
    "nerello mascalese",
    "nero d'avola",
    "palomino",
    "petit manseng",
    "petit verdot",
    "petite sirah",
    "pinot blanc",
    "pinot grigio",
    "pinot gris",
    "pinot meunier",
    "pinot noir",
    "pinotage",
    "primitivo",
    "riesling",
    "rondinella",
    "roussanne",
    "sagrantino",
    "saperavi",
    "sangiovese",
    "savagnin",
    "sauvignon blanc",
    "schiava",
    "semillon",
    "silvaner",
    "shiraz",
    "syrah",
    "tempranillo",
    "touriga franca",
    "touriga nacional",
    "trebbiano",
    "verdejo",
    "verdelho",
    "vermentino",
    "viognier",
    "viura",
    "zinfandel",
}

SWEETNESS_KEYWORDS = {
    "Off-dry": (
        "off-dry",
        "off dry",
        "semi-dry",
        "semi dry",
        "semi-sweet",
        "semi sweet",
        "semisweet",
        "feinherb",
        "halbtrocken",
    ),
    "Sweet": (
        "sweet",
        "demi-sec",
        "doux",
        "dolce",
        "dulce",
        "late harvest",
        "late-harvest",
        "ice wine",
        "icewine",
        "eiswein",
        "vendange tardive",
        "beerenauslese",
        "trockenbeerenauslese",
    ),
    "Dry": (
        "dry",
        "brut nature",
        "extra brut",
        "brut",
        "trocken",
    ),
}

wines = []

# return sweetness by checking name for sweetness keywords
def map_sweetness(name):
    name_lower = str(name or "").casefold()
    for sweetness, keywords in SWEETNESS_KEYWORDS.items():
        if any(re.search(rf"\b{re.escape(keyword)}\b", name_lower) for keyword in keywords):
            return sweetness
    return "Unknown"

# return grape list by checking name for grape keywords
def map_grapes(name):
    name_lower = str(name or "").casefold()
    grapes = []
    for grape in GRAPE_TYPES:
        if grape in name_lower:
            grapes.append(grape)
    return grapes


# return alcohol content as either "high" "medium" or "low"
def map_alcohol(percent):
    try:
        percent = float(percent)
    except (TypeError, ValueError) as error:
        raise ValueError(f"ABV must be a numeric percentage, got {percent!r}") from error
    if percent <= 12.5:
        return "Low"
    if percent <= 13.5:
        return "Medium"
    return "High"


# fetch data rom open API
def fetch():
    seen_entries.clear()

    with httpx.Client(timeout=15.0) as client:
        # get list of wines (our catalog)
        url = "https://vinofyi.com/api/v1/wines/"
        catalog = []
        for _ in range(0,PAGES+1):
            response = client.get(url)
            response.raise_for_status()
            page = response.json()
            catalog.extend(page["results"])
            url = page["next"]
            
        # have threads randomly sample from our query
        # these threads will then build our wine JSON
        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = [
                pool.submit(random_thread, catalog)
                for _ in range(MASTER_DATA_SIZE)
            ]
            for future in futures:
                # throw away result
                future.result()

    with open('Data\\master_wine_data.json', "w") as file:
        json.dump(wines, file, indent=4)
    
# Thread to query catalog and then write it's result into json
def random_thread(catalog):
    global grape_id
    while True:
        wine = random.choice(catalog)
        wine_id = wine.get("id")
        if wine_id is None:
            raise ValueError("Wine record is missing its API id")

        # verify the distinctness of our random draw
        with _WRITE_LOCK:
            if wine_id in seen_entries:
                continue
            seen_entries[wine_id] = True
            break

    name = wine.get("name")
    abv = wine.get("abv")
    wine_data = {
        "wine": name,
        "grapes": map_grapes(name),
        "sweetness": map_sweetness(name),
        "type": wine.get("wine_type"),
        "acidity": wine.get("acidity"),
        "abv": map_alcohol(float(abv)),
        "country_name": wine.get("country_name"),
        "body": wine.get("body"),
        "winery_name": wine.get("winery_name"),
        "region_name": wine.get("region_name")
    }
    with _WRITE_LOCK:
        # save grapes in grape hashset
        for grape in wine_data.get("grapes"):
            if not grape in query_grapes:
                query_grapes[grape] = id
                grape_id+=1
        wines.append(wine_data)

# returns a list of all distinct grapes recorded during fetch
def get_grapes():
    return query_grapes
    