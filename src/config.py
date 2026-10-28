"""Seuils de decision, en pourcentage pour rester coherents quel que soit le prix du produit.

gap_pct = (prix Pixmania - prix du concurrent le moins cher) / prix du concurrent le moins cher * 100
"""

THRESHOLDS = {
    "high_gap_pct": 6.0,         # >= 6 % plus cher que le moins cher -> URGENT
    "medium_gap_pct": 3.0,       # >= 3 % -> A SURVEILLER
    "opportunity_gap_pct": 3.0,  # <= -3 % (moins cher que tous) -> OPPORTUNITE
    "min_margin_pct": 5.0,       # marge minimale acceptable si on s'aligne
    "low_stock_units": 10,       # stock faible en dessous de ce seuil
    "high_stock_units": 100,     # stock eleve au-dessus de ce seuil
}
