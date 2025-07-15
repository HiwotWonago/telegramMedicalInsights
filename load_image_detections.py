import pandas as pd
from sqlalchemy import create_engine

# Load CSV
#df = pd.read_csv('data/processed/image_detections.csv')
df = pd.read_csv('C:/Users/Hiwi/telegramMedicalInsights/src/enrichment/data/processed/image_detections.csv')

# PostgreSQL connection info – CHANGE THESE VALUES
db_config = {
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost',
    'port': '5432',
    'database': 'medical_insights'
}

# Create SQLAlchemy engine
engine = create_engine(
    f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
)

# Load the data into a new table
df.to_sql('image_detections', engine, schema='public', if_exists='replace', index=False)

print("image_detections table loaded into PostgreSQL.")
