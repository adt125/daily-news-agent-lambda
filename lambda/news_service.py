import feedparser

AI_RSS = "https://news.google.com/rss/search?q=artificial+intelligence"
MARKET_RSS = "https://news.google.com/rss/search?q=stock+market+india"


def fetch_rss(url, limit=5):
    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries[:limit]:
        articles.append({"title": entry.title, "link": entry.link})

    return articles


def format_news(articles):
    return "\n".join([f"{a['title']} - {a['link']}" for a in articles])


def get_news():
    ai_articles = fetch_rss(AI_RSS, 5)
    market_articles = fetch_rss(MARKET_RSS, 5)

    ai_news = format_news(ai_articles)
    market_news = format_news(market_articles)

    return (ai_news, market_news)


if __name__ == "__main__":
    print(get_news())
