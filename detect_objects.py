import os 
from ultralytics import YOLO
from pathlib import Path
import pandas as pd
from PIL import Image

# Image directory and output
IMAGE_DIR = Path("data/raw/telegram_images/2025-07-13/media/lobelia4cosmetics")
OUTPUT_CSV = Path("data/processed/image_detections.csv")

# Load pre-trained YOLOv8 model
model = YOLO("yolov8n.pt")

# Store detections
detections = []

print(f"🔍 Scanning images in {IMAGE_DIR}")
for image_file in IMAGE_DIR.glob("*.jpg"):
    print(f"🖼️  Processing: {image_file.name}")
    results = model(image_file)

    for result in results:
        if result.boxes and len(result.boxes.cls) > 0:
            for box in result.boxes:
                cls_id = int(box.cls[0])
                cls_name = result.names[cls_id]
                conf = float(box.conf[0])
                detections.append({
                    "image_name": image_file.name,
                    "detected_object_class": cls_name,
                    "confidence_score": round(conf, 4)
                })
        else:
            print(f"❌ No objects detected in {image_file.name}")

# Save if detections exist
if detections:
    os.makedirs(OUTPUT_CSV.parent, exist_ok=True)
    df = pd.DataFrame(detections)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ Saved {len(df)} detections to {OUTPUT_CSV}")
else:
    print("⚠️ No objects detected in any image. CSV will not be written.")
