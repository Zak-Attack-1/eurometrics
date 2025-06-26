import pandas as pd
from sqlalchemy import create_engine

# Load cleaned data
df = pd.read_csv("C:/Users/lenovo/eurometrics/data/cleaned_ecb_hicp.csv")


# Database connection settings
db_user = "postgres"
db_pass = "Rlzahinmyh3art"   # ← Replace with your actual PostgreSQL password
db_host = "localhost"
db_port = "5432"
db_name = "eurometrics"

# Connect using SQLAlchemy
engine = create_engine(
    f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
)

# Insert data into the hicp_inflation table
df.to_sql("hicp_inflation", engine, if_exists="append", index=False)

print("✅ Data inserted into PostgreSQL successfully.")
