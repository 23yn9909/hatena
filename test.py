import feedparser
import os
import html

def escape_ampersand(text):
    return html.escape(text)

urls = [
    "https://b.hatena.ne.jp/q/%E6%8A%80%E8%A1%93?date_range=5y&users=100&target=tag&sort=recent&mode=rss",
    "https://b.hatena.ne.jp/q/%E4%BB%95%E4%BA%8B?mode=rss&target=tag&users=100&sort=recent&date_range=5y",
    "https://b.hatena.ne.jp/q/%E9%96%8B%E7%99%BA?sort=recent&mode=rss&target=tag&date_range=5y&users=100",
    "https://b.hatena.ne.jp/q/%E6%95%99%E8%82%B2?mode=rss&target=tag&users=100&sort=recent&date_range=5y",
]

unique_entries = []
for url in urls:
    feed = feedparser.parse(url)
    items = []
    for entry in feed.entries:
        print(entry.keys())