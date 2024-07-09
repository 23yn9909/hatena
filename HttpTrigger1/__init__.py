import logging
import feedparser
import os
import html
import datetime
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    urls = [
        "https://b.hatena.ne.jp/q/ai?date_range=5y&users=50&target=tag&sort=recent&mode=rss",
        "https://b.hatena.ne.jp/q/%E6%8A%80%E8%A1%93?date_range=5y&users=50&target=tag&sort=recent&mode=rss",
        "https://b.hatena.ne.jp/q/%E7%A0%94%E7%A9%B6?date_range=5y&users=50&target=tag&sort=recent&mode=rss",
        "https://b.hatena.ne.jp/q/%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0?date_range=5y&users=50&target=tag&sort=recent&mode=rss",
        "https://b.hatena.ne.jp/q/%E4%BB%95%E4%BA%8B?mode=rss&target=tag&users=50&sort=recent&date_range=5y",
        "https://b.hatena.ne.jp/q/%E9%96%8B%E7%99%BA?sort=recent&mode=rss&target=tag&date_range=5y&users=50",
        "https://b.hatena.ne.jp/q/%E6%95%99%E8%82%B2?mode=rss&target=tag&users=50&sort=recent&date_range=5y",
    ]

    unique_entries = []
    items = []
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            try:
                # すでに取得した記事と重複しているかどうかを判定
                if entry.link in [i["link"] for i in unique_entries]:
                    continue
                item = f"""<item rdf:about="{entry['link']}">
                <title>{entry['title']}</title>
                <link>{entry['link']}</link>
                <description></description>
                <content:encoded>{entry['content'][0]['value']}</content:encoded>
                <hatena:bookmarkCommentListPageUrl>{entry.get('hatena_bookmarkcommentlistpageurl', '')}</hatena:bookmarkCommentListPageUrl>
                <hatena:bookmarkcount>{entry.get('hatena_bookmarkcount', '')}</hatena:bookmarkcount>
                <hatena:bookmarkSiteEntriesListUrl>{entry.get('hatena_bookmarksiteentrieslisturl', '')}</hatena:bookmarkSiteEntriesListUrl>
                <hatena:imageurl>{entry.get('hatena_imageurl', '')}</hatena:imageurl>
                </item>
                """
                items.append({
                    "link": entry["link"],
                    "item": item,
                })
                unique_entries.append(entry)
            except Exception as e:
                logging.error(f"Error: Failed to process entry {entry.link}: {str(e)}")

    bun = "\n".join([i["item"] for i in items])
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://purl.org/rss/1.0/" xmlns:admin="http://webns.net/mvcb/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:hatena="http://www.hatena.ne.jp/info/xmlns#" xmlns:syn="http://purl.org/rss/1.0/modules/syndication/" xmlns:taxo="http://purl.org/rss/1.0/modules/taxonomy/">
<channel rdf:about="https://hatena.azurewebsites.net/hatena.rss">
<title>Hatena Feed</title>
<link>https://hatena.azurewebsites.net/hatena.rss</link>
<description>Hatena Feed</description>
<items>
<rdf:Seq>
{"".join([f"<rdf:li rdf:resource='{entry['link']}'/>" for entry in items])}
</rdf:Seq>
</items>
</channel>
{bun}
</rdf:RDF>"""
    return func.HttpResponse(rss)