import streamlit as st

from data.universe import get_nse_universe
from engine.indicators import get_stock_data, add_indicators
from engine.scoring import compute_score
from services.news import get_news
from services.sentiment import sentiment_score
from utils.helpers import generate_signal

st.set_page_config(
    page_title="NSE 4-Week Stock Scanner",
    layout="wide"
)

st.title("📊 NSE 4-Week Investment Opportunity Scanner")
st.write("AI-powered stock ranking system using technical + news sentiment signals")

# Load universe
stocks = get_nse_universe()

results = []

# Button
if st.button("🚀 Run Stock Analysis"):

    progress = st.progress(0)

    for i, ticker in enumerate(stocks):

        try:
            # 1. Price data
            df = get_stock_data(ticker)
            df = add_indicators(df)

            # 2. News + sentiment
            news = get_news(ticker.replace(".NS", ""))
            sentiment = sentiment_score(news)

            # 3. Score
            score = compute_score(df, sentiment)
            signal = generate_signal(score)

            # 4. Entry / Target / Stoploss
            entry = float(df["Close"].iloc[-1])
            target = round(entry * (1 + (score - 50) / 200), 2)
            stoploss = round(entry * 0.95, 2)

            results.append({
                "Stock": ticker,
                "Signal": signal,
                "Score": score,
                "Entry": round(entry, 2),
                "Target": target,
                "Stoploss": stoploss
            })

        except Exception:
            continue

        # progress bar update
        progress.progress((i + 1) / len(stocks))

    st.success("Analysis Completed ✅")

    # Sort results by score (best opportunities first)
    results = sorted(results, key=lambda x: x["Score"], reverse=True)

    st.subheader("📌 Top Stock Opportunities")

    st.dataframe(results, use_container_width=True)

    # Top 5 highlight
    st.subheader("🔥 Top 5 Picks")

    for r in results[:5]:
        st.markdown(
            f"""
            **{r['Stock']}**  
            👉 Signal: {r['Signal']}  
            📊 Score: {r['Score']}  
            🎯 Entry: {r['Entry']} | Target: {r['Target']} | SL: {r['Stoploss']}
            ---
            """
        )

else:
    st.info("Click the button above to scan the market")
