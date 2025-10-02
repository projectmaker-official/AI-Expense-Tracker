# main.py
import streamlit as st
import json
import bcrypt
import utils.app as app

# Load hashed password
with open("config/auth.json", "r") as f:
    auth_data = json.load(f)

stored_hash = auth_data['hashed_password']

# Streamlit page
st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("💸 Expense Tracker 💸🧾💵")

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    password = st.text_input("Enter Password", type="password")
    if st.button("Submit"):
        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            st.session_state['authenticated'] = True
        else:
            st.error("Incorrect Password")

if st.session_state['authenticated']:
    # Import and run your app logic
    app.run()
