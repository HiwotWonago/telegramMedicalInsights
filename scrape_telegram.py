import os
import json
from datetime import datetime
from telethon.sync import TelegramClient
from dotenv import load_dotenv

# Load API credentials from .env
load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
phone = os.getenv("TELEGRAM_PHONE")

# Telegram channels to scrape
channels = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma"
]

# Start a Telegram client session
client = TelegramClient("session", api_id, api_hash)

def sanitize_filename(url):
    return url.split("/")[-1]

async def scrape_channel(channel_url, limit=100):
    await client.start(phone)
    entity = await client.get_entity(channel_url)
    messages = []

    date_str = datetime.today().strftime("%Y-%m-%d")
    channel_name = sanitize_filename(channel_url)
    
    # Paths for raw data + media
    base_path = f"data/raw/telegram_messages/{date_str}"
    os.makedirs(base_path, exist_ok=True)
    
    media_folder = os.path.join(base_path, "media", channel_name)
    os.makedirs(media_folder, exist_ok=True)

    async for message in client.iter_messages(entity, limit=limit):
        media_path = None
        if message.media:
            # Download media file
            media_path = await client.download_media(message.media, file=media_folder)
        
        messages.append({
            "id": message.id,
            "date": message.date.isoformat() if message.date else None,
            "text": message.message,
            "sender_id": message.sender_id,
            "has_media": message.media is not None,
            "media_type": type(message.media).__name__ if message.media else None,
            "media_path": media_path  # local path or None
        })

    # Prepare output folder and file
    date_str = datetime.today().strftime("%Y-%m-%d")
    channel_name = sanitize_filename(channel_url)
    os.makedirs(f"data/raw/telegram_messages/{date_str}", exist_ok=True)
    
    with open(f"data/raw/telegram_messages/{date_str}/{channel_name}.json", "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

    print(f"Scraped {len(messages)} messages from {channel_name}")

# Run scraping for each channel
if __name__ == "__main__":
    import asyncio
    async def main():
        channels = [
            "https://t.me/lobelia4cosmetics",
            "https://t.me/tikvahpharma"
        ]
        for url in channels:
            await scrape_channel(url)
    asyncio.run(main())
