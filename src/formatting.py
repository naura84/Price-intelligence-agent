def format_gap(item):
    """Ecart signe lisible : +50€ (+5.0%) ou -30€ (-9.4%)."""
    return f"{item['gap_vs_cheapest']:+}€ ({item['gap_percentage']:+.1f}%)"
