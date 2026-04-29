import yfinance as yf
import ta

def get_stock_data(ticker):
    df = yf.download(ticker, period="6mo", interval="1d")
    df.dropna(inplace=True)
    return df


def add_indicators(df):
    df["rsi"] = ta.momentum.RSIIndicator(df["Close"]).rsi()

    macd = ta.trend.MACD(df["Close"])
    df["macd"] = macd.macd()
    df["macd_signal"] = macd.macd_signal()

    df["ema20"] = ta.trend.EMAIndicator(df["Close"], window=20).ema_indicator()
    df["ema50"] = ta.trend.EMAIndicator(df["Close"], window=50).ema_indicator()

    df["vol_avg"] = df["Volume"].rolling(20).mean()

    return df
