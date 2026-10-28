from src.config import THRESHOLDS


def _stock_level(stock, t):
    if stock < t["low_stock_units"]:
        return "LOW"
    if stock > t["high_stock_units"]:
        return "HIGH"
    return "NORMAL"


def _classify(gap_pct, t):
    if gap_pct >= t["high_gap_pct"]:
        return "URGENT - Prix trop élevé", "HIGH"
    if gap_pct >= t["medium_gap_pct"]:
        return "ATTENTION - Légèrement sur-coté", "MEDIUM"
    if gap_pct <= -t["opportunity_gap_pct"]:
        return "OPPORTUNITÉ - Pixmania moins cher", "OPPORTUNITY"
    return "OK - Prix compétitif", "LOW"


def analyze_price_gaps(catalog, thresholds=None):
    """Compare chaque produit Pixmania aux concurrents.

    Les seuils sont en pourcentage (voir src/config.py). Si le catalogue
    contient `cost_price`, on calcule aussi la marge et on indique si
    Pixmania peut s'aligner sur le moins cher sans passer sous la marge minimale.
    """
    t = thresholds or THRESHOLDS
    analysis = []

    for product in catalog:
        competitors = product["competitors"]
        if not competitors:
            raise ValueError(f"Aucun concurrent pour : {product['product']}")

        price = product["pixmania_price"]
        min_price = min(competitors.values())
        avg_price = sum(competitors.values()) / len(competitors)
        cheapest = min(competitors, key=competitors.get)

        gap = price - min_price
        gap_pct = round(gap / min_price * 100, 4)
        gap_avg = price - avg_price
        gap_avg_pct = gap_avg / avg_price * 100

        status, priority = _classify(gap_pct, t)

        cost = product.get("cost_price")
        if cost is not None:
            margin_pct = (price - cost) / price * 100
            margin_at_cheapest_pct = (min_price - cost) / min_price * 100
            can_match = margin_at_cheapest_pct >= t["min_margin_pct"]
        else:
            margin_pct = margin_at_cheapest_pct = can_match = None

        analysis.append({
            "product": product["product"],
            "category": product["category"],
            "market": product["market"],
            "pixmania_price": price,
            "min_competitor_price": min_price,
            "cheapest_competitor": cheapest,
            "avg_competitor_price": round(avg_price, 2),
            "gap_vs_cheapest": gap,
            "gap_percentage": round(gap_pct, 1),
            "gap_vs_avg": round(gap_avg, 2),
            "gap_vs_avg_percentage": round(gap_avg_pct, 1),
            "status": status,
            "priority": priority,
            "stock": product["stock_pixmania"],
            "stock_level": _stock_level(product["stock_pixmania"], t),
            "margin_percentage": None if margin_pct is None else round(margin_pct, 1),
            "margin_at_cheapest_percentage": (
                None if margin_at_cheapest_pct is None else round(margin_at_cheapest_pct, 1)
            ),
            "can_match_cheapest": can_match,
        })

    return analysis
