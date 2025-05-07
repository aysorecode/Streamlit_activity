import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text


st.title("🗃️ Streamlit + MySQL Integration")


def get_connection():


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
