import streamlit as st
import pandas as pd



# Load CSV once for reuse
csv_path = r"D:\synthetic_dataset_with_categoricals.csv"
try:
    df_csv = pd.read_csv(csv_path)
except FileNotFoundError:
    df_csv = None
    st.error(f"❌ CSV file not found at: {csv_path}")

st.title("📄 Local CSV Viewer with Filtering")
st.header("Loading and Interacting with CSV Data")

if df_csv is not None:
    if df_csv.shape[1] < 5:
        st.warning("⚠️ CSV file has less than 5 columns.")
    else:
        if st.checkbox("Show raw data"):
            st.subheader("📊 Raw Data:")
            st.dataframe(df_csv)

        column_to_filter = st.selectbox("Select a column to filter by:", df_csv.columns)
        unique_values = df_csv[column_to_filter].dropna().unique()
        selected_value = st.selectbox(f"Select a value from '{column_to_filter}':", sorted(unique_values.astype(str)))

        filtered_df = df_csv[df_csv[column_to_filter].astype(str) == selected_value]
        st.subheader("🔍 Filtered Data:")
        st.dataframe(filtered_df)
