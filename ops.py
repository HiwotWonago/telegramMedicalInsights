from dagster import op
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(["python", "src/scraper/scrape_telegram.py"], check=True)

@op
def load_raw_to_postgres():
    subprocess.run(["python", "src/loader/load_image_detections.py"], check=True)

@op
def run_dbt_transformations():
    subprocess.run(["dbt", "run", "--project-dir", "medical_insights_dbt"], check=True)

@op
def run_yolo_enrichment():
    subprocess.run(["python", "src/enrichment/detect_objects.py"], check=True)
