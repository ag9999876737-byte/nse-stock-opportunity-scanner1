import yfinance as yf
import pandas as pd
import ta


def get_stock_data(ticker):
    try:
        df = yf.download(ticker, period="6mo", interval="1d", progress=False)

        if df is None or df.empty:
            return None

        # 🚨 FIX: force 1D series (VERY IMPORTANT)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        return df

    except Exception:
        return None


def add_indicators(df):
    df = df.copy()

    # 🚨 CRITICAL FIX: ensure 1D Series
    close = df["Close"].squeeze()
    high = df["High"].squeeze()
    low = df["Low"].squeeze()

    # RSI
    df["rsi"] = ta.momentum.RSIIndicator(close=close).rsi()

    # MACD
    macd = ta.trend.MACD(close=close)
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()

    # EMA
    df["ema20"] = ta.trend.EMAIndicator(close=close, window=20).ema_indicator()
    df["ema50"] = ta.trend.EMAIndicator(close=close, window=50).ema_indicator()

    # Volume handling (safe)
    df["vol_avg"] = df["Volume"].rolling(20).mean()

    return df
