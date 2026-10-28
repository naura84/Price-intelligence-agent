from typing import Any
from src.analyzer import analyze_price_gaps


class PriceTools:
    """Les outils que l'agent pourra appeler. Chaque methode = un outil."""

    def __init__(self, catalog):
        self.catalog = catalog
        self.analysis = analyze_price_gaps(catalog)

    def list_at_risk_products(self, min_priority="MEDIUM"):
        levels = ["HIGH"] if min_priority == "HIGH" else ["MEDIUM", "HIGH"]
        keys = ("product", "priority", "gap_percentage", "stock_level", "can_match_cheapest")
        return [
            {k: p[k] for k in keys}
            for p in self.analysis
            if p["priority"] in levels
        ]


TOOL_SCHEMAS: list[Any] = [
    {
        "type": "function",
        "function": {
            "name": "list_at_risk_products",
            "description": (
                "Liste les produits dont le prix Pixmania est plus élevé que celui du "
                "concurrent le moins cher. À utiliser en premier, pour savoir sur quels "
                "produits agir. Renvoie pour chacun : la priorité, l'écart en %, le niveau "
                "de stock et si Pixmania peut s'aligner sur le moins cher sans passer "
                "sous la marge minimale."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "min_priority": {
                        "type": "string",
                        "enum": ["MEDIUM", "HIGH"],
                        "description": "HIGH = seulement les cas urgents. MEDIUM = urgents + à surveiller.",
                    }
                },
                "required": [],
            },
        },
    }
]