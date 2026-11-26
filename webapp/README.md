# Trading Skills Web App

A Streamlit app that takes a trader from zero to an advanced, rule-based process,
with virtual money first. The tool pages call the same Python code the Claude skills
use, so the numbers match the CLI output.

## Training (zero → advanced)

| Level | Focus | Unlocks when | Max risk / demo trade |
|-------|-------|--------------|-----------------------|
| 1 Beginner | Candles, trend, support/resistance, stop-loss, 1% rule | Basics quiz ≥ 80% | 0.5% |
| 2 Risk Control | R-multiples, reward:risk, position sizing | 10 Chart Replay trades | 1% |
| 3 Trend & Context | Market breadth, RSI/ATR, expectancy | 10 closed demo trades with positive expectancy | 1% |
| 4 Advanced | Screeners and setups from the skill catalog | (top level) | 2% |

| Page | What it does |
|------|--------------|
| 🎓 Learning Path | Lessons per level, quiz, progress toward the next level |
| ⏪ Chart Replay | A random stock (ticker and dates hidden) stops at a past date; buy with stop/target or skip, then the next 20 days are revealed and scored in R |
| 💼 Demo Account | Paper trading on real daily prices. Long only, stop-loss and a written reason required, risk capped by level, pre-trade checklist, stops/targets auto-checked on each new daily bar, journal and equity curve |

Progress and the demo account are stored locally in `state/webapp/` (git-ignored).
Replay fills are conservative: gaps through the stop fill at the open, and a bar that
touches both stop and target counts as a stop.

## Tools

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
│   ├── training.py   # levels, lessons, quiz, replay scoring, progress
│   ├── demo_account.py # paper-trading ledger and risk rules
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
