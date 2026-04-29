def generate_signal(score):
    if score >= 70:
        return "🟢 BUY"
    elif score <= 40:
        return "🔴 SELL"
    else:
        return "🟡 HOLD"
