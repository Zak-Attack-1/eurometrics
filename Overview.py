import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# Set page config with EU theme
st.set_page_config(
    page_title="EuroMetrics Dashboard", 
    layout="wide",
    page_icon="🇪🇺"
)

# Custom CSS for EU theme
st.markdown("""
<style>
    /* EU Blue color scheme */
    .main > div {
        padding-top: 2rem;
    }
    
    .stMetric > div > div > div > div {
        background-color: #003399;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FFDD00;
    }
    
    .stSelectbox > div > div > div {
        background-color: #f8f9ff;
    }
    
    .stMultiSelect > div > div > div {
        background-color: #f8f9ff;
    }
    
    .sidebar .stSelectbox > div > div > div {
        background-color: #e6f2ff;
    }
    
    h1 {
        color: #003399;
        border-bottom: 3px solid #FFDD00;
        padding-bottom: 0.5rem;
    }
    
    h2, h3 {
        color: #003399;
    }
    
    .stAlert > div {
        background-color: #003399;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# DB connection function
@st.cache_data
def load_data():
    try:
        conn = psycopg2.connect(
            dbname="eurometrics",
            user="postgres",
            password="Rlzahinmyh3art",
            host="localhost",
            port="5432"
        )
        query = "SELECT * FROM core_economic_indicators;"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return pd.DataFrame()

# Store data in session state for use across pages
if 'df' not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

# Check if data loaded successfully
if df.empty:
    st.error("No data available. Please check your database connection.")
    st.stop()

# Page navigation
st.sidebar.title("🇪🇺 EuroMetrics Dashboard")
st.sidebar.markdown("---")

# Debug: Show available columns
with st.sidebar.expander("Available Columns"):
    st.write(df.columns.tolist())

st.sidebar.markdown("---")

# Sidebar filters (shared across pages)
st.sidebar.header("Filter Data")

# Check for possible region/country column names
region_columns = [col for col in df.columns if any(keyword in col.lower() for keyword in ['region', 'country', 'nation', 'area'])]

if region_columns:
    region_col = region_columns[0]  # Use the first matching column
    st.sidebar.info(f"Using column: {region_col}")
    countries = df[region_col].unique().tolist()
    selected_countries = st.sidebar.multiselect(
        f"Select {region_col.title()}", 
        countries, 
        default=countries
    )
else:
    st.sidebar.error("No region/country column found. Please check your data structure.")
    selected_countries = []
    region_col = None

years = sorted(df['year'].unique())
year_range = st.sidebar.slider(
    "Year Range", 
    min_value=min(years), 
    max_value=max(years), 
    value=(min(years), max(years))
)

# Store filters in session state
st.session_state.selected_countries = selected_countries
st.session_state.year_range = year_range
st.session_state.region_col = region_col

# Filter data
if region_columns and selected_countries:
    filtered_df = df[
        (df[region_col].isin(selected_countries)) &
        (df['year'].between(year_range[0], year_range[1]))
    ]
else:
    filtered_df = df[df['year'].between(year_range[0], year_range[1])]

st.session_state.filtered_df = filtered_df

# Main page content
st.title("EuroMetrics: Economic Overview 🇪🇺")
st.markdown("### European Economic Metrics Dashboard")

# Check if filtered data is available
if filtered_df.empty:
    st.warning("No data available for the selected filters.")
else:
    # Key metrics
    latest_year = filtered_df['year'].max()
    latest_data = filtered_df[filtered_df['year'] == latest_year]
    
    st.subheader(f"Key Metrics for {latest_year}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gdp_sum = latest_data['gdp_eur_millions'].sum()
        st.metric("GDP (Million EUR)", f"{gdp_sum:,.0f}")
    
    with col2:
        avg_hicp = latest_data['avg_hicp_index'].mean()
        st.metric("Average Inflation (HICP)", f"{avg_hicp:.2f}")
    
    with col3:
        population_sum = latest_data['population'].sum()
        st.metric("Population", f"{population_sum:,.0f}")
    
    # Charts with EU color theme
    st.subheader("Economic Trends")
    
    # EU color palette for charts
    eu_colors = ['#003399', '#FFDD00', '#CC0000', '#009900', '#FF6600', '#9900CC', '#00CCCC']
    
    # Line chart: GDP
    if region_columns and selected_countries:
        fig_gdp = px.line(
            filtered_df, 
            x="year", 
            y="gdp_eur_millions", 
            color=region_col, 
            title="GDP Over Time (Million EUR)",
            markers=True,
            color_discrete_sequence=eu_colors
        )
    else:
        fig_gdp = px.line(
            filtered_df, 
            x="year", 
            y="gdp_eur_millions", 
            title="GDP Over Time (Million EUR)",
            markers=True,
            color_discrete_sequence=['#003399']
        )
    
    fig_gdp.update_layout(
        height=500,
        plot_bgcolor='rgba(248,249,255,0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color='#003399',
        title_font_size=18
    )
    st.plotly_chart(fig_gdp, use_container_width=True)
    
    # Line chart: GDP per Capita
    if region_columns and selected_countries:
        fig_capita = px.line(
            filtered_df, 
            x="year", 
            y="gdp_per_capita", 
            color=region_col, 
            title="GDP Per Capita Over Time",
            markers=True,
            color_discrete_sequence=eu_colors
        )
    else:
        fig_capita = px.line(
            filtered_df, 
            x="year", 
            y="gdp_per_capita", 
            title="GDP Per Capita Over Time",
            markers=True,
            color_discrete_sequence=['#003399']
        )
    
    fig_capita.update_layout(
        height=500,
        plot_bgcolor='rgba(248,249,255,0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color='#003399',
        title_font_size=18
    )
    st.plotly_chart(fig_capita, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Tip**: Use the navigation in the sidebar to explore different sections of the dashboard. 🇫🇷 🇩🇪")