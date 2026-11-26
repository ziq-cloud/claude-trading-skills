# Trading Skills Web App

A Streamlit web front end for the skills in this repository. Each page calls the
same Python code the Claude skills use, so the numbers match the CLI output.

| Page | What it does | Skill / data source | API key |
|------|--------------|---------------------|---------|
| 📊 Price Chart | Candles, SMA 20/50/200, volume, RSI 14, ATR 14 | Twelve Data, falls back to yfinance | Optional (`TWELVEDATA_API_KEY`) |
| 🧮 Position Sizer | Share count from stop-loss, ATR or Kelly, with portfolio constraints | `skills/position-sizer` | None |
| 🌡️ Market Breadth | 0–100 breadth health score, components, key levels | `skills/market-breadth-analyzer` (public CSV) | None |
| 📚 Skill Catalog | Browse and filter every skill by category and paid-API need | `skills-index.yaml` | None |

The Price Chart page can pass the latest close and ATR straight into the Position Sizer.

## Run

```bash
# from the repository root
pip install -r webapp/requirements.txt
streamlit run webapp/app.py
```

Open http://localhost:8501.

### Optional environment variables

| Variable | Purpose |
|----------|---------|
| `TWELVEDATA_API_KEY` | Twelve Data key for price data (free tier works). Without it, yfinance is used. |
| `BREADTH_DETAIL_URL`, `BREADTH_SUMMARY_URL` | Point Market Breadth at a CSV mirror instead of the default public URLs. |

Market Breadth reports are written to `reports/webapp/market_breadth/` (git-ignored).

## Layout

```
webapp/
├── app.py            # Streamlit entry point and navigation
├── core/             # Pure logic, no Streamlit (unit tested)
│   ├── catalog.py    # skills-index.yaml loader + filters
│   ├── sizing.py     # position-sizer skill wrapper
│   ├── breadth.py    # market-breadth-analyzer runner + report parser
│   ├── prices.py     # Twelve Data / yfinance OHLCV fetch
│   └── indicators.py # SMA, RSI, ATR
├── views/            # One module per page
└── tests/
```

## Tests

```bash
python3 -m pytest webapp/tests -q
```

## Adding a skill page

1. Put the logic in `core/<name>.py`. Import the skill script or run it as a subprocess
   with `--output-dir`, then read its JSON report.
2. Add tests in `tests/`.
3. Create `views/<name>_page.py` with a `render()` function and register it in `app.py`.

> For education and analysis only. This is not financial advice.
