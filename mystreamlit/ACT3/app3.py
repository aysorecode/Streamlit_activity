import streamlit as st
import pandas as pd
csv_path = r"D:\synthetic_dataset_with_categoricals.csv"
try:
    df_csv = pd.read_csv(csv_path)
except FileNotFoundError:
    df_csv = None
    st.error(f"❌ CSV file not found at: {csv_path}")


st.title("🏢 Data Warehousing & Enterprise Data Management")
st.caption("An interactive overview and data viewer")

st.sidebar.header("⚙️ Options")
show_raw = st.sidebar.checkbox("Show Raw Data")
selected_topic = st.sidebar.selectbox("Select a Focus Area", [
    "Data Warehousing", "Enterprise Data Management", "ETL Process"
])

tab1, tab2 = st.tabs(["📘 Theory", "📊 Data"])  

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📦 Data Warehousing")
        with st.expander("What is a Data Warehouse?"):
            st.write("""
                A data warehouse is a centralized repository for storing integrated data from multiple sources.
                It supports analytical reporting, structured queries, and decision making.
            """)
        with st.expander("Key Characteristics"):
            st.markdown("- Subject-Oriented\n- Integrated\n- Time-Variant\n- Non-volatile")

    with col2:
        st.subheader("🏗️ Enterprise Data Management (EDM)")
        with st.expander("What is EDM?"):
            st.write("""
                EDM is the practice of ensuring that an organization's data is accurate, accessible, consistent, and secure.
                It involves governance, architecture, integration, and metadata management.
            """)
        with st.expander("Core Areas"):
            st.markdown("- Data Governance\n- Master Data Management\n- Metadata Management\n- Data Quality")

with tab2:
    st.subheader("📁 Sample Data Viewer")
    if df_csv is not None and df_csv.shape[1] >= 5:
        if show_raw:
            with st.expander("🔍 Raw Data Preview"):
                st.dataframe(df_csv)

        filter_col = st.sidebar.selectbox("Filter by Column:", df_csv.columns)
        if df_csv[filter_col].dropna().nunique() > 0:
            unique_vals = df_csv[filter_col].dropna().unique()
            selected_val = st.sidebar.selectbox("Select a Value:", sorted(unique_vals.astype(str)))
            filtered_df = df_csv[df_csv[filter_col].astype(str) == selected_val]
            st.write(f"🔎 Showing results for **{filter_col} = {selected_val}**")
            st.dataframe(filtered_df)
        else:
            st.info(f"No unique values found in {filter_col}")
