# Forex Trading Trainer (web app)

A Streamlit app that takes a trader from zero to an advanced, rule-based process with
virtual money first. It covers **major forex pairs, gold, bitcoin and WTI crude oil only**,
with **fixed lot sizes**, buy and sell, leverage and margin.

> For education only. This is not financial advice, and it is not a broker.

## Instruments

| Instrument | Contract per 1.00 lot | Pip | Leverage | Price data |
|------------|-----------------------|-----|----------|------------|
| EUR/USD, GBP/USD, AUD/USD, NZD/USD, USD/CHF, USD/CAD | 100,000 units | 0.0001 | 1:100 | Twelve Data → Yahoo |
| USD/JPY | 100,000 units | 0.01 | 1:100 | Twelve Data → Yahoo |
| XAU/USD (gold) | 100 oz | 0.1 | 1:100 | Twelve Data → Yahoo `GC=F` |
| BTC/USD | 1 BTC | 1 | 1:20 | Twelve Data → Yahoo `BTC-USD` |
| WTI crude oil | 1,000 barrels | 0.01 | 1:100 | Yahoo `CL=F` (Twelve Data's WTI needs a paid plan) |

Contract sizes follow common retail-broker specs; real brokers differ. Prices are **daily**
closes, so this is a swing-trading trainer, not an intraday one. Spreads, swaps and
commissions are not modelled.

**Fixed volume:** trades use one of `0.01, 0.02, 0.05, 0.10, 0.20, 0.50, 1.00` lots. The app
suggests the largest size whose stop-loss risk fits your level's limit and your free margin.

## Demo account

| Type | Balance options | Contract | Display |
|------|-----------------|----------|---------|
| Standard | $100 – $1,000 | 1 lot = full contract | `$1,000.00` |
| Cent | 10,000 – 1,000,000 USC ($100 – $10,000) | 1 lot = 1/100 contract | `100,000 USC` |

* Buy or sell; a stop-loss and a written reason are required; a pre-trade checklist.
* Leverage 1:100 (BTC 1:20). Opening a trade reserves margin; the balance changes when it closes.
* Balance, equity, used and free margin, margin level. **Stop-out at 50%** closes the worst
  losing trade.
* Stops and targets are checked against each new daily bar (gaps fill at the open; a bar
  touching both counts as the stop).
* Journal with equity curve, win rate and expectancy in R.

On a small standard account, even 0.01 lot can exceed a 0.5–1% risk limit, and the app
blocks the trade and says why. That is deliberate: it is the reason cent accounts exist.

## Training (zero → advanced)

| Level | Lessons | Unlocks when | Max risk / demo trade |
|-------|---------|--------------|-----------------------|
| 1 Beginner | Candles, trend, support/resistance, stop-loss, 1% rule | Basics quiz ≥ 80% | 0.5% |
| 2 Risk Control | R-multiples, reward:risk, lots and pips, leverage and margin | 10 Chart Replay trades | 1% |
| 3 Trend & Context | News and sessions, RSI/ATR, expectancy | 10 closed demo trades with positive expectancy | 1% |
| 4 Advanced | Setups, process over outcome | (top level) | 2% |

| Page | What it does |
|------|--------------|
| 🎓 Learning Path | Lessons per level, quiz, progress |
| ⏪ Chart Replay | A random instrument (name and dates hidden) stops at a past date; buy or sell with stop/target, or skip; the next 20 days are revealed and scored in R |
| 💼 Demo Account | Paper trading as above |
| 📊 Price Chart | Candles, SMA 20/50/200, RSI 14, ATR 14 in pips |
| 🧮 Lot Calculator | Stop distance in pips, pip value, exact lot, fixed lot to use, risk and margin for every fixed size |

Progress and the demo account are stored locally in `state/webapp/` (git-ignored).

## Languages

English, Bahasa Melayu, தமிழ் (Tamil) and 中文 (Simplified Chinese). Pick one in the
sidebar; it is kept in the `?lang=` URL parameter (`en`, `ms`, `ta`, `zh`). All strings live
in `core/i18n.py`, and `tests/test_i18n.py` fails if a key is missing a language or its
placeholders differ.

## Run

```bash
# from the repository root
pip install -r webapp/requirements.txt
streamlit run webapp/app.py
```

Open http://localhost:8501. Set `TWELVEDATA_API_KEY` (free tier) for forex, gold and BTC;
without it, Yahoo Finance is used for everything.

## Layout

```
webapp/
├── app.py              # Streamlit entry point, navigation, language picker
├── core/               # Pure logic, no Streamlit (unit tested)
│   ├── instruments.py  # contract specs, pip value, margin, fixed lot sizes
│   ├── demo_account.py # leveraged paper-trading ledger, stop-out
│   ├── training.py     # levels, quiz answers, replay scoring, progress
│   ├── i18n.py         # all UI text in four languages
│   ├── prices.py       # Twelve Data / Yahoo daily OHLC
│   └── indicators.py   # SMA, RSI, ATR
├── views/              # One module per page + shared helpers
└── tests/
```

## Tests

```bash
python3 -m pytest webapp/tests -q
```
