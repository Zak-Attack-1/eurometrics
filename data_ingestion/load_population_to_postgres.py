import pandas as pd
from sqlalchemy import create_engine

def load_population():
    # 1. Read the cleaned CSV
    df = pd.read_csv("C:/Users/lenovo/eurometrics/data/cleaned_population.csv")

    # 2. Connect to your PostgreSQL “eurometrics” database
    engine = create_engine(
        "postgresql+psycopg2://postgres:Rlzahinmyh3art@localhost:5432/eurometrics"
    )

    # 3. Replace the table population_data
    df.to_sql("population_data", engine, if_exists="replace", index=False)
    print("✅ Loaded cleaned_population.csv into table population_data")

if __name__ == "__main__":
    load_population()
