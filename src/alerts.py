def generate_alerts(analysis):
    """
    Identifie et formate les alertes critiques.
    """
    urgent = [p for p in analysis if p["priority"] == "HIGH"]
    opportunities = [p for p in analysis if p["priority"] == "OPPORTUNITY"]
    
    alerts = {
        "urgent_count": len(urgent),
        "opportunity_count": len(opportunities),
        "urgent_products": urgent,
        "opportunities": opportunities
    }
    
    return alerts
