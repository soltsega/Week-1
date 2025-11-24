# Analysis script

This folder contains `analysis.py`, a small script that:

- Loads CSV files from `data/yfinance_data/Data/` (expects `Date, Open, High, Low, Close, Volume`).
- Computes technical indicators using TA-Lib if available (SMA, EMA, RSI, MACD), otherwise falls back to pandas implementations.
- Attempts to use `pynance` for additional metrics if installed; otherwise computes basic metrics (annual return, volatility, Sharpe).
- Saves indicator plots to `demo/figures/`.

Quick run (from repo root, with your virtualenv activated):

```bash
python scripts/analysis.py
```

If TA-Lib isn't installed, the script will still run using pandas fallbacks. Installing TA-Lib on Windows may require the C library; consider using `conda install -c conda-forge ta-lib` if you have conda.
