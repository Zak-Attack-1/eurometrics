import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="Comparative Analysis", page_icon="🇪🇺", layout="wide")

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

st.title("Comparative Analysis")
st.markdown("### Compare economic indicators across regions and time periods")

# Get data from session state
if 'filtered_df' not in st.session_state:
    st.error("Please go to the main page first to load the data.")
    st.stop()

df = st.session_state.filtered_df
region_col = st.session_state.region_col

if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# Comparison controls
st.subheader("Comparison Settings")

# EU color palette
eu_colors = ['#003399', '#FFDD00', '#CC0000', '#009900', '#FF6600', '#9900CC', '#00CCCC']

col1, col2 = st.columns(2)

with col1:
    metrics_to_compare = st.multiselect(
        "Select Metrics to Compare",
        ['gdp_eur_millions', 'gdp_per_capita', 'avg_hicp_index', 'population'],
        default=['gdp_per_capita', 'avg_hicp_index']
    )

with col2:
    comparison_type = st.radio(
        "Comparison Type",
        ["By Region", "By Year", "Correlation Analysis"]
    )

if not metrics_to_compare:
    st.warning("Please select at least one metric to compare.")
    st.stop()

# Comparison visualizations
if comparison_type == "By Region" and region_col:
    st.subheader("Regional Comparison")
    
    # Latest year comparison
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year]
    
    for metric in metrics_to_compare:
        if metric in latest_data.columns:
            st.subheader(f"{metric.replace('_', ' ').title()} - {latest_year}")
            
            fig = px.bar(
                latest_data,
                x=region_col,
                y=metric,
                title=f"{metric.replace('_', ' ').title()} by Region ({latest_year})",
                color=metric,
                color_continuous_scale="Blues"
            )
            fig.update_layout(
                height=400,
                plot_bgcolor='rgba(248,249,255,0.8)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font_color='#003399'
            )
            st.plotly_chart(fig, use_container_width=True)

elif comparison_type == "By Year":
    st.subheader("Year-over-Year Comparison")
    
    for metric in metrics_to_compare:
        if metric in df.columns:
            st.subheader(f"{metric.replace('_', ' ').title()} Trends")
            
            if region_col:
                fig = px.line(
                    df,
                    x='year',
                    y=metric,
                    color=region_col,
                    title=f"{metric.replace('_', ' ').title()} Over Time by Region",
                    markers=True,
                    color_discrete_sequence=eu_colors
                )
            else:
                yearly_avg = df.groupby('year')[metric].mean().reset_index()
                fig = px.line(
                    yearly_avg,
                    x='year',
                    y=metric,
                    title=f"Average {metric.replace('_', ' ').title()} Over Time",
                    markers=True,
                    color_discrete_sequence=['#003399']
                )
            
            fig.update_layout(
                height=400,
                plot_bgcolor='rgba(248,249,255,0.8)',
                paper_bgcolor='rgba(0,0,0,0)',
                title_font_color='#003399'
            )
            st.plotly_chart(fig, use_container_width=True)

elif comparison_type == "Correlation Analysis":
    st.subheader("Correlation Analysis")
    
    if len(metrics_to_compare) >= 2:
        # Correlation matrix
        correlation_data = df[metrics_to_compare].corr()
        
        fig_corr = px.imshow(
            correlation_data,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix",
            color_continuous_scale="Blues"
        )
        fig_corr.update_layout(
            height=500,
            title_font_color='#003399'
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Scatter plots for pairs
        if len(metrics_to_compare) == 2:
            metric1, metric2 = metrics_to_compare
            
            if region_col:
                fig_scatter = px.scatter(
                    df,
                    x=metric1,
                    y=metric2,
                    color=region_col,
                    size='population' if 'population' in df.columns else None,
                    title=f"{metric1.replace('_', ' ').title()} vs {metric2.replace('_', ' ').title()}"
                )
            else:
                fig_scatter = px.scatter(
                    df,
                    x=metric1,
                    y=metric2,
                    title=f"{metric1.replace('_', ' ').title()} vs {metric2.replace('_', ' ').title()}"
                )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("Please select at least 2 metrics for correlation analysis.")

# Summary statistics
st.subheader("Summary Statistics")

summary_stats = df[metrics_to_compare].describe()
st.dataframe(summary_stats, use_container_width=True)

# Ranking table
if region_col and comparison_type == "By Region":
    st.subheader("Regional Rankings 🇫🇷 🇩🇪")
    
    latest_year = df['year'].max()
    latest_data = df[df['year'] == latest_year]
    
    for metric in metrics_to_compare:
        if metric in latest_data.columns:
            ranking = latest_data.groupby(region_col)[metric].mean().sort_values(ascending=False).reset_index()
            ranking['Rank'] = range(1, len(ranking) + 1)
            ranking = ranking[['Rank', region_col, metric]]
            
            st.subheader(f"Top Rankings - {metric.replace('_', ' ').title()}")
            st.dataframe(ranking, use_container_width=True, hide_index=True)