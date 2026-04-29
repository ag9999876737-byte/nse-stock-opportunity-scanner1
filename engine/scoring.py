def compute_score(df, news_sentiment):
    latest = df.iloc[-1]

    score = 0

    # Trend
    if latest["ema20"] > latest["ema50"]:
        score += 25
    else:
        score -= 20

    # RSI
    if 40 < latest["rsi"] < 65:
        score += 20
    elif latest["rsi"] > 70:
        score -= 15

    # MACD
    if latest["macd"] > latest["macd_signal"]:
        score += 15
    else:
        score -= 10

    # Volume
    if latest["Volume"] > latest["vol_avg"]:
        score += 10

    # News
    score += news_sentiment * 30

    # Normalize
    score = max(0, min(100, score + 50))

    return round(score, 2)
