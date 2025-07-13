import json

date_folder = "2025-07-13"  
channel_file = "lobelia4cosmetics.json"

file_path = f"data/raw/telegram_messages/{2025-07-13}/{channel_file}"
with open(file_path, "r", encoding="utf-8") as f:
    messages = json.load(f)

print(f"Loaded {len(messages)} messages from {channel_file}")
print("Sample message:")
print(messages[0])
