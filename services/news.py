import feedparser

def get_news(query):
    try:
        url = f"https://news.google.com/rss/search?q={query}+stock+india"
        feed = feedparser.parse(url)

        return [entry.title for entry in feed.entries[:5]]

    except Exception:
        return []
