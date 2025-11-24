import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

try:
    import talib as ta
    TALIB_AVAILABLE = True
except Exception:
    TALIB_AVAILABLE = False

try:
    import pynance as pn
    PYNANCE_AVAILABLE = True
except Exception:
    PYNANCE_AVAILABLE = False


def load_yfinance_data(folder_path):
    """Load all CSVs from a folder into a single DataFrame.

    Expects CSVs with at least: Date, Open, High, Low, Close, Volume
    Adds a `Symbol` column derived from the filename.
    """
    csvs = glob.glob(os.path.join(folder_path, "*.csv"))
    if not csvs:
        raise FileNotFoundError(f"No CSV files found in {folder_path}")

    frames = []
    for path in csvs:
        df = pd.read_csv(path)
        # normalize column names
        df.columns = [c.strip() for c in df.columns]
        # common column fallbacks
        if 'Date' not in df.columns and 'date' in df.columns:
            df = df.rename(columns={'date': 'Date'})
        # ensure required columns
        required = {'Date', 'Open', 'High', 'Low', 'Close', 'Volume'}
        if not required.issubset(set(df.columns)):
            raise ValueError(f"File {path} is missing required columns: {required - set(df.columns)}")
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date').reset_index(drop=True)
        symbol = os.path.splitext(os.path.basename(path))[0]
        df['Symbol'] = symbol
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    return combined


def compute_indicators(df):
    """Compute technical indicators and attach them to the DataFrame.

    Adds: SMA_20, EMA_20, RSI_14, MACD, MACD_signal
    """
    df = df.copy()
    close = df['Close'].astype(float)

    if TALIB_AVAILABLE:
        df['SMA_20'] = ta.SMA(close, timeperiod=20)
        df['EMA_20'] = ta.EMA(close, timeperiod=20)
        df['RSI_14'] = ta.RSI(close, timeperiod=14)
        macd, macdsignal, macdhist = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        df['MACD'] = macd
        df['MACD_signal'] = macdsignal
    else:
        # fallbacks using pandas
        df['SMA_20'] = close.rolling(window=20, min_periods=1).mean()
        df['EMA_20'] = close.ewm(span=20, adjust=False).mean()
        # RSI fallback
        delta = close.diff()
        up = delta.clip(lower=0)
        down = -1 * delta.clip(upper=0)
        ma_up = up.rolling(14).mean()
        ma_down = down.rolling(14).mean()
        rs = ma_up / ma_down
        df['RSI_14'] = 100 - (100 / (1 + rs))
        # MACD fallback
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        df['MACD'] = ema12 - ema26
        df['MACD_signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    return df


def compute_financial_metrics(df):
    """Compute simple financial metrics per symbol.

    If `pynance` is available, attempt to use it, otherwise compute basic metrics.
    Returns a DataFrame with metrics for each symbol.
    """
    metrics = []
    for symbol, group in df.groupby('Symbol'):
        group = group.sort_values('Date')
        close = group['Close'].astype(float)
        returns = close.pct_change().dropna()
        ann_return = (1 + returns.mean()) ** 252 - 1 if not returns.empty else np.nan
        ann_vol = returns.std() * np.sqrt(252) if not returns.empty else np.nan
        sharpe = ann_return / ann_vol if ann_vol and not np.isnan(ann_vol) else np.nan

        row = {
            'Symbol': symbol,
            'Annualized Return': ann_return,
            'Annualized Volatility': ann_vol,
            'Sharpe Ratio (approx)': sharpe,
            'Observations': len(group)
        }

        # attempt to use pynance for additional metrics if available
        if PYNANCE_AVAILABLE:
            try:
                # note: pynance API may vary; attempt to access common helpers
                perf = pn.performance.Performance(close)
                row['Max Drawdown'] = perf.max_drawdown()
            except Exception:
                row['Max Drawdown'] = np.nan

        metrics.append(row)

    metrics_df = pd.DataFrame(metrics)
    return metrics_df


def plot_symbol(df_symbol, out_folder=None):
    """Plot price with indicators and RSI for a single symbol."""
    symbol = df_symbol['Symbol'].iloc[0]
    fig, (ax_price, ax_rsi) = plt.subplots(2, 1, figsize=(12, 8), sharex=True,
                                            gridspec_kw={'height_ratios': [3, 1]})

    ax_price.plot(df_symbol['Date'], df_symbol['Close'], label='Close', color='black')
    if 'SMA_20' in df_symbol:
        ax_price.plot(df_symbol['Date'], df_symbol['SMA_20'], label='SMA 20', linestyle='--')
    if 'EMA_20' in df_symbol:
        ax_price.plot(df_symbol['Date'], df_symbol['EMA_20'], label='EMA 20', linestyle=':')

    ax_price.set_title(f"{symbol} Price with SMA/EMA")
    ax_price.legend()
    ax_price.grid(True)

    if 'RSI_14' in df_symbol:
        ax_rsi.plot(df_symbol['Date'], df_symbol['RSI_14'], label='RSI 14', color='purple')
        ax_rsi.axhline(70, color='red', linestyle='--', linewidth=0.7)
        ax_rsi.axhline(30, color='green', linestyle='--', linewidth=0.7)
        ax_rsi.set_ylabel('RSI')
        ax_rsi.grid(True)

    plt.tight_layout()
    if out_folder:
        os.makedirs(out_folder, exist_ok=True)
        out_path = os.path.join(out_folder, f"{symbol}_indicators.png")
        fig.savefig(out_path)
        plt.close(fig)
        return out_path
    else:
        plt.show()
        return None


def main(data_dir=None, out_folder='demo/figures'):
    if data_dir is None:
        data_dir = os.path.join('data', 'yfinance_data', 'Data')

    print(f"Loading data from {data_dir}")
    df = load_yfinance_data(data_dir)
    print(f"Loaded {len(df)} rows for {df['Symbol'].nunique()} symbols")

    df_ind = compute_indicators(df)
    metrics = compute_financial_metrics(df_ind)

    print("Computed indicators and financial metrics:\n", metrics)

    saved = []
    for symbol, group in df_ind.groupby('Symbol'):
        path = plot_symbol(group, out_folder=out_folder)
        if path:
            saved.append(path)

    print(f"Saved {len(saved)} figures to {out_folder}")


if __name__ == '__main__':
    main()
