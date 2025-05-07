import streamlit as st


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
