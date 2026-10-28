def generate_alerts(analysis):
    """Regroupe les produits par niveau de priorite."""
    urgent = [p for p in analysis if p["priority"] == "HIGH"]
    watch = [p for p in analysis if p["priority"] == "MEDIUM"]
    opportunities = [p for p in analysis if p["priority"] == "OPPORTUNITY"]

    return {
        "urgent_count": len(urgent),
        "watch_count": len(watch),
        "opportunity_count": len(opportunities),
        "urgent_products": urgent,
        "watch_products": watch,
        "opportunities": opportunities,
    }
