import json
from pathlib import Path

DEFAULT_CATALOG = Path(__file__).resolve().parents[1] / "data" / "catalog.json"


def load_catalog(path=DEFAULT_CATALOG):
    """Charge le catalogue (liste de produits) depuis un fichier JSON.

    Le chemin est calcule a partir de l'emplacement du code : le script
    fonctionne donc quel que soit le dossier depuis lequel on le lance.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
