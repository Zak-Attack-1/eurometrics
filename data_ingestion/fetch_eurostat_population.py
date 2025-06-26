# data_ingestion/fetch_raw_population.py

import pandas as pd
from eurostat import get_data_df

def fetch_raw_population():
    """
    Fetch the full 'demo_pjan' population dataset from Eurostat
    and save it as a raw CSV for downstream cleaning.
    """
    print("📡 Fetching raw demo_pjan population data via eurostat package...")
    # Grab the complete dataset (including all flags, age groups, sexes, regions, years)
    df = get_data_df('demo_pjan', flags=True)
    
    # Save raw dump for later cleaning
    output_path = "data/raw_demo_pjan_population.csv"
    df.to_csv(output_path)
    print(f"✅ Raw data saved to {output_path}")
    
    return df

if __name__ == "__main__":
    fetch_raw_population()

   

