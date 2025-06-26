# data_ingestion/insert_cleaned_gdp.py

import pandas as pd
from sqlalchemy import create_engine

# Load cleaned data
df = pd.read_csv("data/cleaned_eurostat_gdp.csv")

# PostgreSQL connection URL
engine = create_engine("postgresql+psycopg2://postgres:Rlzahinmyh3art@localhost:5432/eurometrics")

# Insert data
df.to_sql("gdp_eurostat", engine, if_exists="append", index=False)

print("✅ Cleaned GDP data inserted into PostgreSQL.")
