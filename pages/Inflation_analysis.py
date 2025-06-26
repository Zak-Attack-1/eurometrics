import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Inflation Analysis", page_icon="🇪🇺", layout="wide")

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

st.title("Inflation Analysis")
st.markdown("### Detailed analysis of HICP (Harmonised Index of Consumer Prices)")

# Get data from session state
if 'filtered_df' not in st.session_state:
    st.error("Please go to the main page first to load the data.")
    st.stop()

df = st.session_state.filtered_df
region_col = st.session_state.region_col

if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# Inflation metrics
st.subheader("Inflation Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_inflation = df['avg_hicp_index'].mean()
    st.metric("Average HICP", f"{avg_inflation:.2f}")

with col2:
    max_inflation = df['avg_hicp_index'].max()
    st.metric("Highest HICP", f"{max_inflation:.2f}")

with col3:
    min_inflation = df['avg_hicp_index'].min()
    st.metric("Lowest HICP", f"{min_inflation:.2f}")

with col4:
    inflation_range = max_inflation - min_inflation
    st.metric("HICP Range", f"{inflation_range:.2f}")

# Charts with EU color theme
eu_colors = ['#003399', '#FFDD00', '#CC0000', '#009900', '#FF6600', '#9900CC', '#00CCCC']

col1, col2 = st.columns(2)

with col1:
    st.subheader("HICP Over Time")
    if region_col:
        fig_hicp = px.line(
            df, 
            x="year", 
            y="avg_hicp_index", 
            color=region_col,
            title="HICP Index by Region",
            markers=True,
            color_discrete_sequence=eu_colors
        )
    else:
        fig_hicp = px.line(
            df, 
            x="year", 
            y="avg_hicp_index",
            title="HICP Index Over Time",
            markers=True,
            color_discrete_sequence=['#003399']
        )
    fig_hicp.update_layout(
        height=400,
        plot_bgcolor='rgba(248,249,255,0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color='#003399'
    )
    st.plotly_chart(fig_hicp, use_container_width=True)

with col2:
    st.subheader("HICP Distribution")
    if region_col:
        fig_box = px.box(
            df, 
            x=region_col, 
            y="avg_hicp_index",
            title="HICP Distribution by Region",
            color_discrete_sequence=eu_colors
        )
    else:
        fig_box = px.histogram(
            df, 
            x="avg_hicp_index",
            title="HICP Distribution",
            nbins=20,
            color_discrete_sequence=['#003399']
        )
    fig_box.update_layout(
        height=400,
        plot_bgcolor='rgba(248,249,255,0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color='#003399'
    )
    st.plotly_chart(fig_box, use_container_width=True)

# Yearly comparison
st.subheader("Year-over-Year Analysis")

if region_col and len(df[region_col].unique()) > 1:
    # Heatmap of inflation by region and year
    pivot_data = df.pivot_table(
        values='avg_hicp_index', 
        index=region_col, 
        columns='year', 
        aggfunc='mean'
    )
    
    fig_heatmap = px.imshow(
        pivot_data,
        aspect="auto",
        title="HICP Heatmap by Region and Year",
        color_continuous_scale="Blues"
    )
    fig_heatmap.update_layout(
        height=500,
        title_font_color='#003399'
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
else:
    # Simple year-over-year comparison
    yearly_avg = df.groupby('year')['avg_hicp_index'].mean().reset_index()
    fig_yearly = px.bar(
        yearly_avg,
        x='year',
        y='avg_hicp_index',
        title="Average HICP by Year",
        color_discrete_sequence=['#003399']
    )
    fig_yearly.update_layout(
        height=400,
        plot_bgcolor='rgba(248,249,255,0.8)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_font_color='#003399'
    )
    st.plotly_chart(fig_yearly, use_container_width=True)

# Data table
st.subheader("Detailed Data")
if region_col:
    summary_stats = df.groupby([region_col, 'year'])['avg_hicp_index'].agg(['mean', 'min', 'max']).round(2)
    st.dataframe(summary_stats, use_container_width=True)
else:
    yearly_stats = df.groupby('year')['avg_hicp_index'].agg(['mean', 'min', 'max']).round(2)
    st.dataframe(yearly_stats, use_container_width=True)