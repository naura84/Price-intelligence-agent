from src.loader import load_catalog
from src.tools import PriceTools


def test_list_at_risk_products_high_only():
    tools = PriceTools(load_catalog())
    names = [p["product"] for p in tools.list_at_risk_products("HIGH")]
    assert names == ["Sony WH-1000XM5", "PlayStation 5 Slim"]


def test_list_at_risk_products_medium_includes_high():
    tools = PriceTools(load_catalog())
    result = tools.list_at_risk_products("MEDIUM")
    assert len(result) == 5
    assert {"product", "priority", "gap_percentage", "stock_level", "can_match_cheapest"} == set(result[0])