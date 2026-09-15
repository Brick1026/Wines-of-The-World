# Retrieves data from API

import threading
import json
import load

from vinofyi.api import VinoFYI
from concurrent.futures import ThreadPoolExecutor

_WRITE_LOCK = threading.Lock()

# how large of a set of wines do we want
MASTER_DATA_SIZE = 5000

wines = []

def fetch():
    
    pool = ThreadPoolExecutor(max_workers=4)
    # start by querying the VinoFYI database to build a list of 10,000 random wines
    for i in range(0,MASTER_DATA_SIZE+1):
        pool.submit(query_thread)
        
    # cleanup pool
    pool.shutdown(wait=True,cancel_futures=False)
    
    # save our wines into the master_wine json
    with open('Data\\master_wine_data.json', "r+") as file:
        data = json.load(file)
        data["wines"].extend(wines)
        file.seek
        json.dump(data, file, indent=4)
    
    # end the loading screen, we are done
    load.destroy()
    
# Thread to query database and then write it's result into array
def query_thread():
    with VinoFYI as api:
        wine = api.random()
        wine = {
            "wine": wine.get("name"),
            "grape": wine.get("grape"),
            "color": wine.get("color"),
            "notes": wine.get("flavor_notes", []),
            "aged": wine.get("aged", False),
            "pairings": wine.get("pairings", []),
            "sweetness": wine.get("sweetness"),
            "tannins": wine.get("tannins"),
            "body": wine.get("body"),
            "complexity": wine.get("complexity")
        }
        with _WRITE_LOCK:
            wines.append(wine)
    