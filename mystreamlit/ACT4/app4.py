import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

@st.cache_data
def fetch_psgc_data():
    url = "https://psgc.cloud/api/cities-municipalities"
    response = requests.get(url)
    return response.json()

psgc_data = fetch_psgc_data()
df_psgc = pd.DataFrame(psgc_data)

if not df_psgc.empty:
    # Rename columns for clarity
    df_psgc.rename(columns={
        'zip_code': 'ZIP Code',
        'code': 'Code',
        'district': 'District',
        'type': 'Type',
        'region_id': 'Region ID',
        'province_id': 'Province ID'
    }, inplace=True)

    # Sidebar filter
    region_ids = sorted(df_psgc['Region ID'].dropna().unique().astype(str))
    selected_region = st.sidebar.selectbox("📍 Filter by Region ID:", ["All"] + region_ids)

    if selected_region != "All":
        df_psgc = df_psgc[df_psgc['Region ID'].astype(str) == selected_region]

    # Display filtered data
    st.subheader("📋 Filtered Cities/Municipalities")
    st.dataframe(df_psgc)

    # Chart 1: Bar Chart - Count by Type
    st.subheader("1. Bar Chart: Count by Type")
    st.bar_chart(df_psgc['Type'].value_counts())

    # Chart 2: Pie Chart - Distribution by District
    st.subheader("2. Pie Chart: Distribution by District")
    district_counts = df_psgc['District'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(district_counts, labels=district_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

    # Chart 3: Line Chart - Simulated ZIP Growth
    st.subheader("3. Line Chart: Simulated ZIP Growth")
    zip_prefix = df_psgc['ZIP Code'].dropna().astype(str).str[:2]
    zip_counts = zip_prefix.value_counts().head(5)
    growth_df = pd.DataFrame({
        'ZIP Prefix': zip_counts.index,
        '2020': zip_counts.values * 0.8,
        '2021': zip_counts.values * 0.9,
        '2022': zip_counts.values
    }).set_index('ZIP Prefix')

    # Reshape and plot
    growth_df_reset = growth_df.reset_index().melt(id_vars='ZIP Prefix', var_name='Year', value_name='Count')
    fig_line = px.line(growth_df_reset, x='Year', y='Count', color='ZIP Prefix', markers=True,
                       title="Simulated ZIP Growth Over Years")
    st.plotly_chart(fig_line)

    # Chart 4: Heatmap - Region ID vs Type
    st.subheader("4. Heatmap: Region ID vs Type")
    pivot = pd.crosstab(df_psgc['Region ID'], df_psgc['Type'])
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.heatmap(pivot, annot=True, fmt='d', cmap='YlOrBr', ax=ax2)
    st.pyplot(fig2)

    # Chart 5: Scatter Plot - Count per Province ID
    st.subheader("5. Scatter Plot: Count per Province ID")
    province_counts = df_psgc['Province ID'].value_counts().reset_index()
    province_counts.columns = ['Province ID', 'Count']
    fig3 = px.scatter(province_counts, x='Province ID', y='Count', size='Count', color='Province ID')
    st.plotly_chart(fig3)

else:
    st.error("❌ Failed to load PSGC API data.")
