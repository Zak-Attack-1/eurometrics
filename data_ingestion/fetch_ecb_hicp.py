import requests
import pandas as pd
import os
from sqlalchemy import create_engine, text

# Map of ECB REF_AREA codes to our table codes
REGION_MAP = {
    "U2": "EA19",  # Euro Area
    "FR": "FR",    # France
    "DE": "DE"     # Germany
}

# SDMX series template: will replace "U2" dynamically
BASE_URL_TEMPLATE = "https://data-api.ecb.europa.eu/service/data/ICP/M.{ref}.N.000000.4.INX?format=csvdata"

def fetch_all_hicp():
    all_dfs = []
    os.makedirs("data", exist_ok=True)

    # 1. Fetch each region's HICP series
    for ref_area, code in REGION_MAP.items():
        url = BASE_URL_TEMPLATE.format(ref=ref_area)
        print(f"Fetching HICP for {code} via {url}")
        resp = requests.get(url)
        resp.raise_for_status()

        raw_path = f"data/ecb_hicp_{code}.csv"
        with open(raw_path, "wb") as f:
            f.write(resp.content)

        # Load and keep only relevant columns
        df = pd.read_csv(raw_path)
        # Expect columns "TIME_PERIOD" and "OBS_VALUE"
        if "TIME_PERIOD" not in df.columns or "OBS_VALUE" not in df.columns:
            raise ValueError(f"Unexpected columns in HICP CSV for {code}: {df.columns.tolist()}")
        df = df[["TIME_PERIOD", "OBS_VALUE"]].copy()
        df.columns = ["date_str", "hicp_index"]
        # Parse date: TIME_PERIOD is "YYYY-MM", so append "-01"
        df["date"] = pd.to_datetime(df["date_str"] + "-01", format="%Y-%m-%d", errors="coerce")
        df["region"] = code
        # Keep only the final columns
        df = df[["date", "hicp_index", "region"]]
        all_dfs.append(df)

    # 2. Concatenate all regions
    full_df = pd.concat(all_dfs, ignore_index=True)

    # 3. Save combined cleaned CSV locally
    clean_path = "data/cleaned_ecb_hicp_all.csv"
    full_df.to_csv(clean_path, index=False)
    print(f"✅ Combined HICP data saved to {clean_path}")

    # 4. Insert into PostgreSQL
    # Update this connection string as needed
    engine = create_engine("postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/eurometrics")

    with engine.begin() as conn:
        # Drop dependent materialized view first, if it exists
        conn.execute(text("DROP MATERIALIZED VIEW IF EXISTS economic_indicators;"))
        # Drop hicp_inflation table if exists (so we can recreate via to_sql)
        conn.execute(text("DROP TABLE IF EXISTS hicp_inflation;"))

    # Write the table from scratch
    # to_sql with if_exists='replace' will create the table
    full_df.to_sql("hicp_inflation", engine, if_exists="replace", index=False)
    print("✅ hicp_inflation table created and data inserted.")

    # 5. (Optional) Recreate the materialized view economic_indicators here.
    # If you want the script to also rebuild the view immediately, uncomment and adjust the block below:
    """
    with engine.begin() as conn:
        conn.execute(text(\"\"\"
            CREATE MATERIALIZED VIEW economic_indicators AS
            SELECT 
                g.geo AS country_code,
                EXTRACT(YEAR FROM g.year)::INT AS year,
                ROUND(g.value, 2) AS gdp_eur,
                ROUND(h.hicp_index, 2) AS hicp_index
            FROM 
                gdp_eurostat g
            JOIN 
                (
                    SELECT 
                        region AS geo,
                        EXTRACT(YEAR FROM date)::INT AS year,
                        AVG(hicp_index) AS hicp_index
                    FROM hicp_inflation
                    GROUP BY region, year
                ) h
              ON g.geo = h.geo AND EXTRACT(YEAR FROM g.year)::INT = h.year;
        \"\"\" ))
    print("✅ economic_indicators materialized view recreated.")
    """

if __name__ == "__main__":
    fetch_all_hicp()

