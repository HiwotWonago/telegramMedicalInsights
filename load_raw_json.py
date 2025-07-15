import os
import json
import psycopg2
from datetime import datetime
from pathlib import Path

# Database config
DB_CONFIG = {
    "host": "localhost",
    "dbname": "medical_insights",
    "user": "postgres",
    "password": "1234",  # 🔐 Replace this with your real password
    "port": 5432
}

# Path to the folder containing JSON files
BASE_DIR = Path(__file__).resolve().parents[1] / "data" / "raw" / "telegram_messages"/"2025-07-13"


def load_json_to_postgres():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    for date_folder in BASE_DIR.iterdir():
        if not date_folder.is_dir():
            continue

        for json_file in date_folder.glob("*.json"):
            print(f"📥 Loading: {json_file}")
            with open(json_file, "r", encoding="utf-8") as f:
                try:
                    messages = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"❌ Skipping {json_file}: JSON decode error: {e}")
                    continue

            for msg in messages:
                try:
                    message_id = int(msg.get("id"))
                    date = msg.get("date")
                    date = datetime.fromisoformat(date) if date else None
                    sender = msg.get("sender", {}).get("username", "")
                    message = msg.get("message", "")
                    media_type = msg.get("media", {}).get("type", "") if "media" in msg else None
                    media_path = msg.get("media", {}).get("file", "") if "media" in msg else None
                    channel_name = json_file.stem  # filename (e.g., lobelia4cosmetics)
                    json_payload = json.dumps(msg)

                    cursor.execute("""
                        INSERT INTO raw.telegram_messages (
                            message_id, date, sender, message, media_type, media_path, channel_name, json_payload
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (message_id) DO NOTHING;
                    """, (
                        message_id, date, sender, message,
                        media_type, media_path, channel_name, json_payload
                    ))

                except Exception as e:
                    print(f"❌ Error inserting message from {json_file.name}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print(" Done loading all JSON files into raw.telegram_messages")

if __name__ == "__main__":
    load_json_to_postgres()

