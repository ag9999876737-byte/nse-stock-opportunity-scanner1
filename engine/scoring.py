def compute_score(df, news_sentiment):
    latest = df.iloc[-1]

    score = 50  # base

    # Trend
    if latest["ema20"] > latest["ema50"]:
        score += 20
    else:
        score -= 15

    # RSI
    if 40 <= latest["rsi"] <= 65:
        score += 15
    elif latest["rsi"] > 70:
        score -= 10

    # MACD
    if latest["macd"] > latest["macd_signal"]:
        score += 10

    # Volume
    if latest["Volume"] > latest["vol_avg"]:
        score += 10

    # News impact
    score += news_sentiment * 25

    return max(0, min(100, round(score, 2)))
