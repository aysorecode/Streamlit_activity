import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sqlalchemy import create_engine, text
import cv2
import numpy as np
from PIL import Image
import time
# Set page configuration (only once!)
# Set page configuration (only once!)
st.set_page_config(page_title="Streamlit Multi-Problem App", layout="wide")

# # Load CSV once for reuse
# csv_path = r"D:\sir_paulin\cleaned_synthetic.csv"
# try:
#     df_csv = pd.read_csv(csv_path)
# except FileNotFoundError:
#     df_csv = None
#     st.error(f"❌ CSV file not found at: {csv_path}")

# ----------- Problem 1: User Input -------------
st.title("👋 Welcome to My Streamlit App")
st.header("User Input and Dynamic Output")

name = st.text_input("Enter your name:")
age = st.number_input("Enter your age:", min_value=0, max_value=120, step=1)

if name:
    st.write(f"Hello, **{name}**! 👋")
    st.write(f"You are **{int(age)}** years old.")
    if age < 18:
        st.write("You're a minor. 🚸")
    elif age < 65:
        st.write("You're an adult. 🧑‍💼")
    else:
        st.write("You're a senior citizen. 👵🧓")

# ----------- Problem 2: Local CSV Viewer -------------
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

# ----------- Problem 3: EDM & DW with Tabs -------------
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

# ----------- Problem 4: PSGC Cities Dashboard -------------
st.title("📍 PSGC Cities and Municipalities Dashboard")

# Fetch data from PSGC API
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

#problem 5
# ----------------------------
# Configuration
# ----------------------------
st.title("🗃️ Streamlit + MySQL Integration")

# ----------------------------
# DB Connection
# ----------------------------
def get_connection():
    # Replace with your own MySQL DB credentials
    host = "localhost"
    user = "admin"
    password = "admin"
    database = "Project"
    port = 3306
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")
    return engine

engine = get_connection()

# ----------------------------
# Bonus: Simple Authentication
# ----------------------------
users = {"admin": "admin123", "user1": "password1"}

with st.sidebar:
    st.header("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if username in users and users[username] == password:
        st.success(f"Welcome, {username} ✅")
        logged_in = True
    else:
        logged_in = False
        if username or password:
            st.error("❌ Invalid credentials")

if logged_in:

    # ----------------------------
    # View / Filter Data
    # ----------------------------
    st.subheader("📋 View Data From Table")
    table_name = st.text_input("Enter table name to query:", "your_table")

    try:
        with engine.connect() as conn:
            df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
            st.write(f"Total rows: {df.shape[0]}")
            if not df.empty:
                selected_col = st.selectbox("Filter by column", df.columns)
                unique_vals = df[selected_col].dropna().unique()
                selected_val = st.selectbox("Select value", unique_vals.astype(str))
                filtered = df[df[selected_col].astype(str) == selected_val]
                st.dataframe(filtered)
            else:
                st.warning("Table is empty.")
    except Exception as e:
        st.error(f"Error: {e}")

    # ----------------------------
    # Insert New Row
    # ----------------------------
    st.subheader("➕ Insert New Row")
    with st.form("insert_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, step=1)
        city = st.text_input("City")
        submitted = st.form_submit_button("Insert")

        if submitted:
            try:
                with engine.begin() as conn:
                    query = text(f"INSERT INTO {table_name} (name, age, city) VALUES (:name, :age, :city)")
                    conn.execute(query, {"name": name, "age": age, "city": city})
                    st.success("✅ Row inserted successfully!")
            except Exception as e:
                st.error(f"❌ Error inserting data: {e}")

else:
    st.warning("🔒 Please login to access the dashboard.")

#problem 6
st.title("🎥 OpenCV + Streamlit: Real-Time Video Processing")

# -------------------------------
# Sidebar Controls
# -------------------------------
st.sidebar.header("⚙️ Filter Controls")
selected_filter = st.sidebar.selectbox("Select Filter", ["None", "Grayscale", "Canny Edge", "Face Detection"])

if selected_filter == "Canny Edge":
    threshold1 = st.sidebar.slider("Threshold 1", 0, 255, 100)
    threshold2 = st.sidebar.slider("Threshold 2", 0, 255, 200)

# -------------------------------
# Load Face Detection Model
# -------------------------------
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# -------------------------------
# Video Capture
# -------------------------------
capture = cv2.VideoCapture(0)

frame_placeholder = st.empty()
snapshot_btn = st.button("📸 Take Snapshot")

snapshot_img = None

while True:
    ret, frame = capture.read()
    if not ret:
        st.error("Unable to access webcam.")
        break

    frame = cv2.flip(frame, 1)  # Mirror the image

    # Apply selected filter
    if selected_filter == "Grayscale":
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)

    elif selected_filter == "Canny Edge":
        frame = cv2.Canny(frame, threshold1, threshold2)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)

    elif selected_filter == "Face Detection":
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display frame
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_placeholder.image(frame_rgb, channels="RGB")

    # Snapshot logic
    if snapshot_btn:
        snapshot_img = frame_rgb.copy()
        break

    # Small delay to avoid high CPU usage
    time.sleep(0.03)

capture.release()

# -------------------------------
# Display Snapshot
# -------------------------------
if snapshot_img is not None:
    st.success("✅ Snapshot captured!")
    st.image(snapshot_img, caption="📸 Snapshot", use_column_width=True)