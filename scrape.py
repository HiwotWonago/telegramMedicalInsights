import os
import json
import logging
from datetime import datetime
from telethon.sync import TelegramClient
from dotenv import load_dotenv

load_dotenv()
api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
phone = os.getenv("TELEGRAM_PHONE")

client = TelegramClient("session", api_id, api_hash)

# Setup logging
logging.basicConfig(
    filename="scrape_telegram.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def sanitize_filename(url):
    return url.split("/")[-1]

async def scrape_channel(channel_url, limit=100):
    try:
        logging.info(f"Starting scrape for channel: {channel_url}")
        await client.start(phone)
        entity = await client.get_entity(channel_url)

        raw_messages = []
        async for message in client.iter_messages(entity, limit=limit):
            raw_messages.append(message.to_dict())  # preserve full raw message dict

        date_str = datetime.today().strftime("%Y-%m-%d")
        channel_name = sanitize_filename(channel_url)
        os.makedirs(f"data/raw/telegram_messages/{date_str}", exist_ok=True)

        file_path = f"data/raw/telegram_messages/{date_str}/{channel_name}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(raw_messages, f, ensure_ascii=False, indent=2)

        logging.info(f"Completed scrape for channel: {channel_url} - {len(raw_messages)} messages saved")

    except Exception as e:
        logging.error(f"Error scraping {channel_url}: {str(e)}", exc_info=True)

if __name__ == "__main__":
    import asyncio

    channels = [
        "https://t.me/lobelia4cosmetics",
        "https://t.me/tikvahpharma"
    ]

    async def main():
        for url in channels:
            await scrape_channel(url)

    asyncio.run(main())
