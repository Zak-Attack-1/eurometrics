import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data Explorer", page_icon="🇪🇺", layout="wide")

# Custom CSS for EU theme
st.markdown("""
<style>
    .stMetric > div > div > div > div {
        background-color: #003399;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FFDD00;
    }
    
    h1 {
        color: #003399;
        border-bottom: 3px solid #FFDD00;
        padding-bottom: 0.5rem;
    }
    
    h2, h3 {
        color: #003399;
    }
</style>
""", unsafe_allow_html=True)

st.title("Data Explorer")
st.markdown("### Explore and analyze your economic data in detail")

# Get data from session state
if 'df' not in st.session_state:
    st.error("Please go to the main page first to load the data.")
    st.stop()

df = st.session_state.df
filtered_df = st.session_state.filtered_df
region_col = st.session_state.region_col

# Data overview
st.subheader("Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Records", len(df))

with col2:
    st.metric("Filtered Records", len(filtered_df))

with col3:
    st.metric("Number of Columns", len(df.columns))

with col4:
    years_span = df['year'].max() - df['year'].min() + 1
    st.metric("Years Covered", years_span)

# Data structure
st.subheader("Data Structure")

col1, col2 = st.columns(2)

with col1:
    st.write("**Column Information:**")
    column_info = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes,
        'Non-Null Count': df.count(),
        'Null Count': df.isnull().sum()
    })
    st.dataframe(column_info, use_container_width=True)

with col2:
    st.write("**Data Quality:**")
    total_cells = len(df) * len(df.columns)
    null_cells = df.isnull().sum().sum()
    completeness = ((total_cells - null_cells) / total_cells) * 100
    
    st.metric("Data Completeness", f"{completeness:.1f}%")
    
    if region_col:
        unique_regions = df[region_col].nunique()
        st.metric("Unique Regions", unique_regions)
    
    unique_years = df['year'].nunique()
    st.metric("Unique Years", unique_years)

# Interactive data exploration
st.subheader("Interactive Data Explorer")

# Column selection
columns_to_show = st.multiselect(
    "Select columns to display:",
    df.columns.tolist(),
    default=df.columns.tolist()[:5]  # Show first 5 columns by default
)

# Sorting options
sort_column = st.selectbox("Sort by:", df.columns.tolist(), index=0)
sort_order = st.radio("Sort order:", ["Ascending", "Descending"])

# Apply sorting
if sort_order == "Ascending":
    display_df = filtered_df[columns_to_show].sort_values(sort_column)
else:
    display_df = filtered_df[columns_to_show].sort_values(sort_column, ascending=False)

# Display data
st.subheader("Filtered Data")
st.dataframe(display_df, use_container_width=True, height=400)

# Download option
csv = display_df.to_csv(index=False)
st.download_button(
    label="📥 Download filtered data as CSV",
    data=csv,
    file_name='eurometrics_filtered_data.csv',
    mime='text/csv'
)

# Statistical summary
st.subheader("Statistical Summary")

numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
if 'year' in numeric_columns:
    numeric_columns.remove('year')  # Remove year from statistical analysis

if numeric_columns:
    selected_numeric_cols = st.multiselect(
        "Select numeric columns for statistical analysis:",
        numeric_columns,
        default=numeric_columns[:3]  # Default to first 3 numeric columns
    )
    
    if selected_numeric_cols:
        stats_df = filtered_df[selected_numeric_cols].describe()
        st.dataframe(stats_df, use_container_width=True)
        
        # Histograms
        st.subheader("Distribution Analysis")
        
        for col in selected_numeric_cols:
            fig = px.histogram(
                filtered_df,
                x=col,
                title=f"Distribution of {col.replace('_', ' ').title()}",
                nbins=30
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

# Missing data analysis
st.subheader("Missing Data Analysis")

missing_data = df.isnull().sum()
missing_data = missing_data[missing_data > 0].sort_values(ascending=False)

if len(missing_data) > 0:
    st.write("**Columns with missing data:**")
    missing_df = pd.DataFrame({
        'Column': missing_data.index,
        'Missing Count': missing_data.values,
        'Missing Percentage': (missing_data.values / len(df) * 100).round(2)
    })
    st.dataframe(missing_df, use_container_width=True, hide_index=True)
    
    # Visualization of missing data
    fig = px.bar(
        missing_df,
        x='Column',
        y='Missing Percentage',
        title="Missing Data by Column (%)"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.success("No missing data found in the dataset!")

# Data search
st.subheader("🔎 Search Data")

search_column = st.selectbox("Search in column:", df.columns.tolist())
search_term = st.text_input(f"Search for values in {search_column}:")

if search_term:
    if df[search_column].dtype == 'object':
        search_results = df[df[search_column].str.contains(search_term, case=False, na=False)]
    else:
        try:
            search_value = float(search_term)
            search_results = df[df[search_column] == search_value]
        except ValueError:
            st.error("Please enter a valid number for numeric columns.")
            search_results = pd.DataFrame()
    
    st.write(f"Found {len(search_results)} matching records:")
    if len(search_results) > 0:
        st.dataframe(search_results, use_container_width=True)