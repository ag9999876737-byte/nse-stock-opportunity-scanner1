import feedparser

def get_news(query):
    url = f"https://news.google.com/rss/search?q={query}+stock+india&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)

    news = []
    for entry in feed.entries[:5]:
        news.append(entry.title)

    return news
