from src.scraper import get_catalog_prices
from src.analyzer import analyze_price_gaps
from src.alerts import generate_alerts
from src.llm_reporter import generate_report


def run_price_intelligence_pipeline():
    """
    Pipeline complet Price Intelligence Agent.
    """
    
    print("=" * 60)
    print("PRICE INTELLIGENCE AGENT — Pixmania")
    print("=" * 60)
    
    #Récupération des données
    print("\nRécupération des données catalogue...")
    catalog = get_catalog_prices()
    print(f"{len(catalog)} produits analysés")
    
    #Analyse des écarts
    print("\nAnalyse comparative des prix...")
    analysis = analyze_price_gaps(catalog)
    
    # Affichage du tableau de bord rapide
    print("\nTABLEAU DE BORD RAPIDE :")
    print("-" * 60)
    for item in analysis:
        print(f"{item['status']}")
        print(f"   {item['product']}")
        print(f"   Pixmania: {item['pixmania_price']}€ | "
              f"Moins cher: {item['cheapest_competitor']} "
              f"({item['min_competitor_price']}€) | "
              f"Écart: +{item['gap_vs_cheapest']}€ "
              f"(+{item['gap_percentage']}%)")
        print()
    
    #Alertes
    alerts = generate_alerts(analysis)
    print(f"{alerts['urgent_count']} alerte(s) urgente(s) détectée(s)")
    print(f"{alerts['opportunity_count']} opportunité(s) identifiée(s)")
    
    #Rapport LLM
    print("\nGénération du rapport IA en cours...")
    print("-" * 60)
    report = generate_report(analysis)
    print("\nRAPPORT INTELLIGENCE PRIX :")
    print("=" * 60)
    print(report)
    print("=" * 60)
    
    return {
        "analysis": analysis,
        "alerts": alerts,
        "report": report
    }


if __name__ == "__main__":
    results = run_price_intelligence_pipeline()