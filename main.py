import feedparser
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime


WORLDWIDE_FEEDS = {
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "KrebsOnSecurity": "https://krebsonsecurity.com/feed/"
}


GERMANY_FEEDS = {
    "heise Security": "https://www.heise.de/security/feed.xml"
}


def get_news(category, source_name, rss_url):

    feed = feedparser.parse(rss_url)

    articles = []

    now = datetime.now(timezone.utc)
    last_24_hours = now - timedelta(hours=24)

    for article in feed.entries:

        if not article.get("published"):
            continue

        try:
            published_time = parsedate_to_datetime(
                article.published
            ).astimezone(timezone.utc)

        except (TypeError, ValueError):
            continue

        if published_time < last_24_hours:
            continue

        article_data = {
            "category": category,
            "source": source_name,
            "title": article.title,
            "published": article.published,
            "url": article.link
        }

        articles.append(article_data)

    return articles

    feed = feedparser.parse(rss_url)

    articles = []

    now = datetime.now(timezone.utc)
    last_24_hours = now - timedelta(hours=24)

    for article in feed.entries:

        if not hasattr(article, "published_parsed"):
            continue

        published_time = datetime.fromtimestamp(
            feedparser.mktime_tz(article.published_parsed),
            timezone.utc
        )

        if published_time < last_24_hours:
            continue

        article_data = {
            "category": category,
            "source": source_name,
            "title": article.title,
            "published": article.get("published", "Unknown"),
            "url": article.link
        }

        articles.append(article_data)

    return articles


print("\n🇩🇪 GERMANY FEED DEBUG")
print("*" * 70)

for source_name, rss_url in GERMANY_FEEDS.items():

    feed = feedparser.parse(rss_url)

    print("Source:", source_name)
    print("Articles available in RSS:", len(feed.entries))

    for article in feed.entries[:5]:
        print("\nTitle:", article.title)
        print("Published:", article.get("published", "Unknown"))

all_articles = []


for source_name, rss_url in WORLDWIDE_FEEDS.items():

    articles = get_news(
        "WORLDWIDE",
        source_name,
        rss_url
    )

    all_articles.extend(articles)


for source_name, rss_url in GERMANY_FEEDS.items():

    articles = get_news(
        "GERMANY",
        source_name,
        rss_url
    )

    all_articles.extend(articles)


""" print("\n🌍🇩🇪 CYBERSECURITY NEWS - LAST 24 HOURS") """
print("\nWorldwide articles:",
      sum(1 for article in all_articles if article["category"] == "WORLDWIDE"))

print("Germany articles:",
      sum(1 for article in all_articles if article["category"] == "GERMANY"))
print("=" * 70)


for article in all_articles:

    print("\nCategory:", article["category"])
    print("Source:", article["source"])
    print("Title:", article["title"])
    print("Published:", article["published"])
    print("URL:", article["url"])

    print("-" * 70)


print("\nTotal recent articles:", len(all_articles))
