from src.loader import load_catalog
from src.analyzer import analyze_price_gaps
from src.alerts import generate_alerts
from src.formatting import format_gap


def run_price_intelligence_pipeline():
    """Pipeline complet Price Intelligence Agent."""

    print("=" * 60)
    print("PRICE INTELLIGENCE AGENT — Pixmania")
    print("=" * 60)

    print("\nRécupération des données catalogue...")
    catalog = load_catalog()
    print(f"{len(catalog)} produits analysés")

    print("\nAnalyse comparative des prix...")
    analysis = analyze_price_gaps(catalog)

    print("\nTABLEAU DE BORD RAPIDE :")
    print("-" * 60)
    for item in analysis:
        print(f"{item['status']}")
        print(f"   {item['product']}")
        print(f"   Pixmania: {item['pixmania_price']}€ | "
              f"Moins cher: {item['cheapest_competitor']} "
              f"({item['min_competitor_price']}€) | "
              f"Écart: {format_gap(item)} | "
              f"Stock: {item['stock']} ({item['stock_level']})")
        print()

    alerts = generate_alerts(analysis)
    print(f"{alerts['urgent_count']} alerte(s) urgente(s) détectée(s)")
    print(f"{alerts['watch_count']} produit(s) à surveiller")
    print(f"{alerts['opportunity_count']} opportunité(s) identifiée(s)")

    # Le rapport IA est optionnel : le tableau de bord reste affiché s'il échoue.
    report = None
    print("\nGénération du rapport IA en cours...")
    print("-" * 60)
    try:
        from src.llm_reporter import generate_report
        report = generate_report(analysis)
        print("\nRAPPORT INTELLIGENCE PRIX :")
        print("=" * 60)
        print(report)
        print("=" * 60)
    except Exception as exc:
        print(f"Rapport IA indisponible ({type(exc).__name__}: {exc})")
        print("Vérifie que les dépendances sont installées (pip install -r requirements.txt) et ta clé API dans .env.")

    return {"analysis": analysis, "alerts": alerts, "report": report}


if __name__ == "__main__":
    run_price_intelligence_pipeline()
