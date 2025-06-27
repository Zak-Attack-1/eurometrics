# EuroMetrics – European Economic Intelligence Dashboard

**EuroMetrics** is a full-stack data analytics project that models and visualizes key macroeconomic indicators—**GDP**, **Inflation (HICP)**, **Population**, and **GDP per Capita**—across **France**, **Germany**, and the **Euro Area** using open Eurostat data.

The pipeline ingests, transforms, and serves data through a rich Streamlit dashboard, offering both high-level insights and detailed exploration.

---

## 📊 Dashboard Pages (Streamlit)

- **Overview**: Macro snapshot of key indicators over time  
- **Comparative Analysis**: Side-by-side country trends for GDP, Inflation, and GDP per Capita  
- **Data Explorer**: Interactive filtering and inspection of the dataset  
- **Inflation Analysis**: Deep dive into HICP inflation trends and cross-country inflation comparison  

---

## 🛠️ Tech Stack

| Component               | Tool / Language             |
|-------------------------|-----------------------------|
| **Ingestion**           | Python (`eurostat`, `pandas`) |
| **Storage**             | PostgreSQL                  |
| **Modeling**            | dbt                         |
| **Validation**          | dbt tests, dbt-utils        |
| **Visualization**       | Streamlit + Altair/Plotly   |
| **Automation (optional)** | Airflow-ready structure    |

---

## 📁 Project Structure

```bash
eurometrics/
├── data/                     # Raw and cleaned CSVs
├── data_ingestion/           # Python scripts for data fetching
│   └── fetch_eurostat_population.py
├── eurometrics_dbt/          # dbt project for modeling
├── logs/                     # Pipeline and run logs
├── notebooks/                # Jupyter notebooks for EDA and testing
├── pages/                    # Additional Streamlit pages
│   ├── Comparative_analysis.py
│   ├── Data_Explorer.py
│   └── Inflation_analysis.py
├── Overview.py               # Main Streamlit app entry point
└── README.md                 # You're here!
```

---

## ⚙️ Setup Instructions

1. **Clone the repo**

```bash
git clone https://github.com/yourusername/eurometrics.git
cd eurometrics
```

2. **Create and activate conda environment**

```bash
conda create -n eurometrics python=3.11
conda activate eurometrics
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run data ingestion**

```bash
python data_ingestion/fetch_eurostat_population.py
```

5. **Set up PostgreSQL database and run dbt models**

```bash
cd eurometrics_dbt
dbt run
dbt test
```

6. **Launch Streamlit app**

```bash
streamlit run Overview.py
```

---

## 📈 Sample Use Cases

* Track how GDP per capita evolved post-COVID across France, Germany, and the Eurozone
* Explore inflation divergence between countries over time
* Enable policy research and investment decisions based on official macroeconomic trends

---

## 🧠 License & Credits

* Data from Eurostat
* Built by Zakaria Alaimia for data science & BI portfolio
* License: MIT

---

## 🚀 Contact

Feel free to connect or collaborate via LinkedIn
