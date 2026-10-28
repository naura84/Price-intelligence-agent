import pytest
from src.analyzer import analyze_price_gaps
from src.alerts import generate_alerts
from src.formatting import format_gap


def make(price, competitors=None, stock=50, cost=None):
    p = {"product": "X", "category": "C", "pixmania_price": price,
         "competitors": {"Amazon": 100} if competitors is None else competitors,
         "stock_pixmania": stock, "market": "FR"}
    if cost is not None:
        p["cost_price"] = cost
    return p


def prio(price):
    return analyze_price_gaps([make(price)])[0]["priority"]


def test_priorities_are_percentage_based():
    assert prio(106) == "HIGH"          # +6 %
    assert prio(103) == "MEDIUM"        # +3 %
    assert prio(101) == "LOW"           # +1 %
    assert prio(97) == "OPPORTUNITY"    # -3 %


def test_same_percentage_same_priority_whatever_the_price():
    cheap = analyze_price_gaps([make(106, {"A": 100})])[0]["priority"]
    expensive = analyze_price_gaps([make(1060, {"A": 1000})])[0]["priority"]
    assert cheap == expensive == "HIGH"


def test_stock_level():
    levels = [analyze_price_gaps([make(100, stock=s)])[0]["stock_level"] for s in (5, 50, 150)]
    assert levels == ["LOW", "NORMAL", "HIGH"]


def test_margin_and_matching():
    r = analyze_price_gaps([make(110, cost=90)])[0]   # min concurrent = 100
    assert r["margin_percentage"] == 18.2
    assert r["margin_at_cheapest_percentage"] == 10.0
    assert r["can_match_cheapest"] is True
    r = analyze_price_gaps([make(110, cost=98)])[0]
    assert r["can_match_cheapest"] is False


def test_missing_cost_price_is_none():
    r = analyze_price_gaps([make(110)])[0]
    assert r["margin_percentage"] is None and r["can_match_cheapest"] is None


def test_no_competitor_raises():
    with pytest.raises(ValueError):
        analyze_price_gaps([make(100, competitors={})])


def test_alert_counts():
    a = generate_alerts(analyze_price_gaps([make(106), make(103), make(97), make(101)]))
    assert (a["urgent_count"], a["watch_count"], a["opportunity_count"]) == (1, 1, 1)


def test_format_gap_signs():
    assert format_gap({"gap_vs_cheapest": 50, "gap_percentage": 5.0}) == "+50€ (+5.0%)"
    assert format_gap({"gap_vs_cheapest": -30, "gap_percentage": -9.4}) == "-30€ (-9.4%)"
