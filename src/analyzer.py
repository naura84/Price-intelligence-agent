def analyze_price_gaps(catalog):
    """
    Analyse les écarts entre Pixmania et les concurrents.
    Identifie les opportunités et les risques.
    """
    analysis = []
    
    for product in catalog:
        pixmania_price = product["pixmania_price"]
        competitors = product["competitors"]
        
        # Prix min et max concurrents
        min_competitor_price = min(competitors.values())
        max_competitor_price = max(competitors.values())
        avg_competitor_price = sum(competitors.values()) / len(competitors)
        cheapest_competitor = min(competitors, key=competitors.get)
        
        # Calcul des écarts
        gap_vs_cheapest = pixmania_price - min_competitor_price
        gap_vs_avg = pixmania_price - avg_competitor_price
        gap_pct = (gap_vs_cheapest / min_competitor_price) * 100
        
        # Classification de la situation
        if gap_vs_cheapest > 50:
            status = "URGENT - Prix trop élevé"
            priority = "HIGH"
        elif gap_vs_cheapest > 20:
            status = "ATTENTION - Légèrement sur-coté"
            priority = "MEDIUM"
        elif gap_vs_cheapest < -30:
            status = "OPPORTUNITÉ - Pixmania moins cher"
            priority = "OPPORTUNITY"
        else:
            status = "OK - Prix compétitif"
            priority = "LOW"
        
        analysis.append({
            "product": product["product"],
            "category": product["category"],
            "pixmania_price": pixmania_price,
            "min_competitor_price": min_competitor_price,
            "cheapest_competitor": cheapest_competitor,
            "avg_competitor_price": round(avg_competitor_price, 2),
            "gap_vs_cheapest": gap_vs_cheapest,
            "gap_percentage": round(gap_pct, 1),
            "status": status,
            "priority": priority,
            "stock": product["stock_pixmania"],
            "market": product["market"]
        })
    
    return analysis
