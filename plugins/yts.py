import feedparser
import re
from pyrogram import Client, filters

def crawl_yts():
    url = "https://yts.mx/rss/0/all/all/0"
    feed = feedparser.parse(url)

    torrents = []
    for entry in feed.entries:
        title = entry.title  # Movie title
        size = parse_size_yts(entry.description)  # Extract size
        link = entry.enclosures[0]["href"]  # Torrent link

        if size:
            torrents.append({
                "title": title,
                "size": size,
                "link": link
            })

    return torrents[:5]  # Limit to the latest 5 torrents

# Extract size from description (YTS format: "<b>Size:</b> 1.2 GB")
def parse_size_yts(description):
    match = re.search(r"<b>Size:</b>\s*([\d.]+\s*[GMK]B)", description)
    return match.group(1) if match else "Unknown"


# Telegram command to fetch and send YTS torrents
@Client.on_message(filters.command("yts"))
async def send_torrents(client, message):
    torrents = crawl_yts()
    if torrents:
        await message.reply_text("\n".join(torrents))
    else:
        await message.reply_text("No torrents found.")
