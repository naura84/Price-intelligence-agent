# Price Intelligence Agent

A price intelligence project that compares Pixmania's prices with competitors', flags at-risk products and opportunities, and generates a business-ready report with an AI model. It currently runs as a pipeline; the goal is to turn it into a real agent (see Roadmap).

## What it does
1. Reads the catalog from [data/catalog.json](data/catalog.json) (simulated data)
2. Computes the gap between Pixmania and each competitor, in euros and in %
3. Classifies each product: urgent, watch, opportunity, or OK
4. Computes the margin and checks whether Pixmania could match the cheapest competitor without going below a minimum margin
5. Generates alerts, then an AI-written report

## Project structure
- [main.py](main.py) — entry point
- [src/loader.py](src/loader.py) — loads the JSON catalog
- [src/config.py](src/config.py) — decision thresholds (in %)
- [src/analyzer.py](src/analyzer.py) — gaps, priorities, stock level, margins
- [src/alerts.py](src/alerts.py) — groups products by priority
- [src/formatting.py](src/formatting.py) — display helpers
- [src/llm_reporter.py](src/llm_reporter.py) — AI report (Gemini API)
- [tests/](tests/) — unit tests for the analysis logic

## Installation
Run the commands one by one.

```bash
python -m venv .venv
```
Activate the environment:
- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- Windows cmd: `.venv\Scripts\activate.bat`
- macOS / Linux: `source .venv/bin/activate`

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Configuration
Copy `.env.example` to `.env` and add your API key:

```env
GEMINI_API_KEY=your_api_key_here
# Optional: GEMINI_MODEL=gemini-3.5-flash-lite
```
Without a key, the dashboard still displays; only the AI report is skipped.

## Run
```bash
python main.py
```

## Tests
```bash
python -m pytest
```

## Decision rules
Gap = (Pixmania price − cheapest competitor) / cheapest competitor. Thresholds are percentages, so a 6 % gap is treated the same on a 100 € accessory and a 1000 € phone (see [src/config.py](src/config.py)):

| Gap vs cheapest | Priority |
|---|---|
| ≥ +6 % | HIGH (urgent) |
| ≥ +3 % | MEDIUM (watch) |
| ≤ −3 % | OPPORTUNITY |
| otherwise | LOW (OK) |

Stock is reported as LOW (< 10), NORMAL, or HIGH (> 100). If `cost_price` is provided, the analysis also returns the current margin, the margin if Pixmania aligned on the cheapest competitor, and whether that alignment keeps at least 5 % margin.

## Data format
```json
{
  "product": "Product name",
  "category": "Category",
  "pixmania_price": 100,
  "cost_price": 80,
  "competitors": {"Amazon FR": 95, "Fnac": 102},
  "stock_pixmania": 50,
  "market": "FR"
}
```
`cost_price` is optional.

## Roadmap
- [x] Percentage-based thresholds, stock level, margins, tests
- [ ] Tools the model can call (list at-risk products, competitor prices, simulate a new price)
- [ ] Agent loop with tool calling and a call log
- [ ] Structured price recommendations with guardrails (minimum margin, human validation)
- [ ] Price history and a real data source

## Limitations
- The catalog is simulated data, not live prices.
- The AI report depends on the input data and on a valid API key.

## License
No license has been defined yet.
