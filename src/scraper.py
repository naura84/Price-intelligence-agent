import json # le module pour lire du JSON

def get_catalog_prices():
    with open("data/catalog.json", "r", encoding="utf-8") as f:
        catalog = json.load(f)
        
    return catalog