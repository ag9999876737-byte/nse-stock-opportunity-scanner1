import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")

sia = SentimentIntensityAnalyzer()

def sentiment_score(news_list):
    if not news_list:
        return 0

    scores = []
    for n in news_list:
        scores.append(sia.polarity_scores(n)["compound"])

    return sum(scores) / len(scores)
