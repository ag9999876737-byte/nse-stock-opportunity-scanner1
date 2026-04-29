import streamlit as st

from data.universe import get_nse_universe
from engine.indicators import get_stock_data, add_indicators
from engine.scoring import compute_score
from services.news import get_news
from services.sentiment import sentiment_score
from utils.helpers import generate_signal

st.set_page_config(page_title="NSE Stock Scanner", layout="wide")

st.title("📊 NSE 4-Week Stock Opportunity Scanner")
st.write("Technical + News Sentiment based ranking system")

stocks = get_nse_universe()

results = []

st.write("Total Stocks in Universe:", len(stocks))

if st.button("🚀 Run Analysis"):

    progress = st.progress(0)

    for i, ticker in enumerate(stocks):

        st.write(f"Analyzing {ticker}")

        df = get_stock_data(ticker)

        # skip invalid data safely
        if df is None or df.empty or len(df) < 50:
            st.warning(f"No/insufficient data: {ticker}")
            continue

        df = add_indicators(df)

        news = get_news(ticker.replace(".NS", ""))
        sentiment = sentiment_score(news)

        score = compute_score(df, sentiment)
        signal = generate_signal(score)

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

        progress.progress((i + 1) / len(stocks))

    st.success("Analysis Completed")

    if len(results) == 0:
        st.error("No results generated. Check data source issues.")
    else:
        results = sorted(results, key=lambda x: x["Score"], reverse=True)

        st.subheader("📌 Top Opportunities")
        st.dataframe(results, use_container_width=True)

        st.subheader("🔥 Top 5 Picks")

        for r in results[:5]:
            st.markdown(f"""
            **{r['Stock']}**  
            👉 {r['Signal']}  
            📊 Score: {r['Score']}  
            🎯 Entry: {r['Entry']} | Target: {r['Target']} | SL: {r['Stoploss']}
            ---
            """)
