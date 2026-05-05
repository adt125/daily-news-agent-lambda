from urllib.request import urlopen
import xml.etree.ElementTree as ET

AI_RSS = "https://news.google.com/rss/search?q=artificial+intelligence"
MARKET_RSS = "https://news.google.com/rss/search?q=stock+market+india"


def fetch_rss(url, limit=5):
    with urlopen(url, timeout=10) as response:
        root = ET.fromstring(response.read())

    articles = []
    for item in root.findall("./channel/item")[:limit]:
        title = item.findtext("title", default="")
        link = item.findtext("link", default="")
        articles.append({"title": title, "link": link})

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
