<?php
function escape_ampersand($text) {
    return htmlspecialchars($text, ENT_QUOTES | ENT_XML1, 'UTF-8');
}

$urls = [
    "https://b.hatena.ne.jp/q/%E6%8A%80%E8%A1%93?date_range=5y&users=100&target=tag&sort=recent&mode=rss",
    "https://b.hatena.ne.jp/q/%E4%BB%95%E4%BA%8B?mode=rss&target=tag&users=100&sort=recent&date_range=5y",
    "https://b.hatena.ne.jp/q/%E9%96%8B%E7%99%BA?sort=recent&mode=rss&target=tag&date_range=5y&users=100",
    "https://b.hatena.ne.jp/q/%E6%95%99%E8%82%B2?mode=rss&target=tag&users=100&sort=recent&date_range=5y",
];

$entries = [];
foreach ($urls as $url) {
    $feed = simplexml_load_file($url);
    foreach ($feed->channel->item as $item) {
        $link = (string) $item->link;
        $title = escape_ampersand((string) $item->title);
        $description = escape_ampersand((string) $item->description);
        $hatena_bookmarkcount = (int) $item->children('http://b.hatena.ne.jp/-/bookmark/')->count;
        $hatena_bookmark_comment_list_page_url = (string) $item->children('http://b.hatena.ne.jp/-/bookmark/')->commentlist;
        $entries[] = [
            "link" => $link,
            "title" => $title,
            "description" => $description,
            "hatena_bookmarkcount" => $hatena_bookmarkcount,
            "hatena_bookmark_comment_list_page_url" => $hatena_bookmark_comment_list_page_url,
        ];
    }
}

$unique_entries = array_values(array_unique($entries, SORT_REGULAR));

$rss = '<?xml version="1.0" encoding="UTF-8"?>' . PHP_EOL .
    '<rss version="2.0">' . PHP_EOL .
    '  <channel>' . PHP_EOL .
    '    <title>Hatena RSS Feed</title>' . PHP_EOL .
    '    <link>https://example.com</link>' . PHP_EOL .
    '    <description>This is a Hatena RSS feed.</description>';

foreach ($unique_entries as $entry) {
    $rss .= PHP_EOL .
        '    <item>' . PHP_EOL .
        '      <title>' . $entry["title"] . '</title>' . PHP_EOL .
        '      <link>' . $entry["link"] . '</link>' . PHP_EOL .
        '      <description>' . $entry["description"] . '</description>' . PHP_EOL .
        '      <hatena_bookmarkcount>' . $entry["hatena_bookmarkcount"] . '</hatena_bookmarkcount>' .
        '      <hatena_bookmarkcount>' . $entry["hatena_bookmarkcount"] . '</hatena_bookmarkcount>' .
        '      <bookmarkCommentListPageUrl>' . $entry["hatena_bookmark_comment_list_page_url"] . '</bookmarkCommentListPageUrl>' . PHP_EOL . ' </item>';
}

$rss .= PHP_EOL . ' </channel>' . PHP_EOL . '</rss>';

file_put_contents('merged.rss', $rss);