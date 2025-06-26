import requests
import os

def fetch_gdp_raw():
    """
    Fetch raw GDP data (annual, market prices in million EUR) for FR, DE, EA19
    from Eurostat's SDMX API and save it as TSV (then optionally convert).
    """
    # Build the URL properly - try TSV format first as it's preferred by Eurostat
    base_url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"
    dataset = "NAMA_10_GDP"
    # Dimensions: FREQ.UNIT.NA_ITEM.GEO
    key = "A.CP_MEUR.B1GQ.FR+DE+EA19"
    
    # Try different format options
    formats_to_try = [
        ("TSV", "data/eurostat_gdp_raw_sdmx.tsv"),
        ("SDMX-CSV", "data/eurostat_gdp_raw_sdmx.csv"),
        ("genericdata", "data/eurostat_gdp_raw_sdmx.xml")
    ]
    
    for format_param, output_path in formats_to_try:
        url = f"{base_url}/{dataset}/{key}?format={format_param}"
        print(f"Trying format {format_param}:")
        print(f"URL: {url}")
        
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            
            os.makedirs("data", exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(resp.content)
            
            print(f"✅ Successfully saved {format_param} data to {output_path}")
            return  # Exit on first success
            
        except requests.exceptions.HTTPError as e:
            print(f"❌ Failed with {format_param} format: {e}")
            continue
    
    print("❌ All formats failed. Check the API documentation or dataset availability.")

def fetch_gdp_raw_simple():
    """
    Alternative: Try the most basic TSV format that Eurostat prefers
    """
    url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/NAMA_10_GDP/A.CP_MEUR.B1GQ.FR+DE+EA19?format=TSV"
    
    print(f"Fetching GDP data with TSV format:\n{url}")
    
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        
        os.makedirs("data", exist_ok=True)
        raw_path = "data/eurostat_gdp_raw.tsv"
        with open(raw_path, "wb") as f:
            f.write(resp.content)
        
        print(f"✅ Saved TSV data to {raw_path}")
        
        # Optionally convert TSV to CSV
        convert_tsv_to_csv(raw_path, "data/eurostat_gdp_raw.csv")
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ Request failed: {e}")
        print("The dataset might not be available or the API structure has changed.")

def convert_tsv_to_csv(tsv_path, csv_path):
    """Convert TSV file to CSV format"""
    try:
        with open(tsv_path, 'r', encoding='utf-8') as tsv_file:
            content = tsv_file.read()
        
        # Replace tabs with commas
        csv_content = content.replace('\t', ',')
        
        with open(csv_path, 'w', encoding='utf-8') as csv_file:
            csv_file.write(csv_content)
        
        print(f"✅ Converted TSV to CSV: {csv_path}")
    except Exception as e:
        print(f"❌ TSV to CSV conversion failed: {e}")

if __name__ == "__main__":
    # Try the comprehensive approach first
    fetch_gdp_raw()
    
    # If that fails, try the simple TSV approach
    print("\nTrying simple TSV approach...")
    fetch_gdp_raw_simple()