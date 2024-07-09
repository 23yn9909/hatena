import feedparser
import re
import os
import html

def escape_ampersand(text):
    return html.escape(text)

def get_content_encoded(entry):
    for elem in entry.get("content", []):
        if elem["type"] == "text/html":
            html = elem["value"]
            return re.search("<content:encoded>(.*?)</content:encoded>", html, re.DOTALL).group(1)
    return ""

urls = [
    "https://b.hatena.ne.jp/q/%E6%8A%80%E8%A1%93?date_range=5y&users=100&target=tag&sort=recent&mode=rss",
    "https://b.hatena.ne.jp/q/%E4%BB%95%E4%BA%8B?mode=rss&target=tag&users=100&sort=recent&date_range=5y",
    "https://b.hatena.ne.jp/q/%E9%96%8B%E7%99%BA?sort=recent&mode=rss&target=tag&date_range=5y&users=100",
    "https://b.hatena.ne.jp/q/%E6%95%99%E8%82%B2?mode=rss&target=tag&users=100&sort=recent&date_range=5y",
]

entries = []
for url in urls:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        #print(entry.keys())
        link = entry["link"]
        title = escape_ampersand(entry["title"])
        description = escape_ampersand(entry["summary"])
        hatena_bookmarkcount = entry["hatena_bookmarkcount"]
        hatena_bookmark_comment_list_page_url = entry["hatena_bookmarkcommentlistpageurl"]
        content = entry["content"]
        entries.append({
            "link": link,
            "title": title,
            "description": description,
            "hatena_bookmarkcount": hatena_bookmarkcount,
            "hatena_bookmark_comment_list_page_url": hatena_bookmark_comment_list_page_url,
            "content": content,
        })

unique_entries = []
for entry in entries:
    if entry not in unique_entries:
        unique_entries.append(entry)

rss = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Hatena RSS Feed</title>
    <link>https://example.com</link>
    <description>This is a Hatena RSS feed.</description>"""

for entry in unique_entries:
    rss += f"""
    <item>
      <title>{entry["title"]}</title>
      <link>{entry["link"]}</link>
      <description>{entry["description"]}</description>
      <hatena_bookmarkcount>{entry["hatena_bookmarkcount"]}</hatena_bookmarkcount>
      <bookmarkCommentListPageUrl>{entry["hatena_bookmark_comment_list_page_url"]}</bookmarkCommentListPageUrl>
      <content>{entry["content"]}</content>
    </item>"""

rss += """
  </channel>
</rss>
"""

print(rss)

with open('merged.rss', 'w', encoding='utf-8') as f:
    f.write(rss)