# Price-intelligente-agent

This project is a price intelligence agent designed to analyze product catalog prices, compare Pixmania’s pricing with competitors, detect at-risk items, and generate a business-ready report.

## Goal

The pipeline helps to:
- retrieve product catalog data,
- compare each Pixmania price with competitor prices,
- identify significant price gaps,
- flag high-priority opportunities and risks,
- produce a natural-language report using an AI model.

## How the pipeline works

The main script runs the following steps:
1. Read the catalog from [data/catalog.json](data/catalog.json)
2. Compute the gap between Pixmania prices and competitor prices
3. Classify products by urgency or opportunity level
4. Generate business alerts
5. Produce an AI-generated report

## Project structure

- [main.py](main.py) — entry point of the pipeline
- [src/scraper.py](src/scraper.py) — loads the JSON catalog
- [src/analyzer.py](src/analyzer.py) — computes price gaps and classifications
- [src/alerts.py](src/alerts.py) — generates alerts
- [src/llm_reporter.py](src/llm_reporter.py) — generates the report using AI
- [data/catalog.json](data/catalog.json) — sample catalog data

## Prerequisites

- Python 3.10+
- An Anthropic account and API key for the AI report generation
- Dependencies listed in [requirements.txt](requirements.txt)

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# or
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

## Configuration

Create a `.env` file at the project root with your API key:

```env
ANTHROPIC_API_KEY=your_api_key_here
```

The code uses this environment variable to initialize the Anthropic client.

## Running the project

Run the pipeline with:

```bash
python main.py
```

The program will display:
- the number of products analyzed,
- the price differences,
- the number of urgent alerts and opportunities,
- the final AI-generated report.

## Data format

The file [data/catalog.json](data/catalog.json) expects entries in the following format:

```json
{
  "product": "Product name",
  "category": "Category",
  "pixmania_price": 100,
  "competitors": {
    "Amazon FR": 95,
    "Fnac": 102
  },
  "stock_pixmania": 50,
  "market": "FR"
}
```

## Example business logic

The project automatically classifies products based on observed gaps:
- price much higher than the cheapest competitor → urgent alert,
- price slightly above the market → watch list,
- price lower than competitors → opportunity.

## Limitations / notes

- The project currently works with a local JSON catalog.
- The quality of the AI report depends on the quality of the input data and the configured API key.
- For production use, it would be useful to add a real data source, persistent storage, and automation.

## License

No specific license has been defined for the repository yet.
