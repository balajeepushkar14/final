import streamlit as st
from database import add_user, authenticate, create_db

create_db()

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        success, role = authenticate(username, password)
        if success:
            st.session_state['username'] = username
            st.session_state['role'] = role
            st.success(f"Logged in as {username} ({role})")
        else:
            st.error("Invalid username or password")

def signup():
    st.subheader("Sign Up")
    username = st.text_input("Choose Username")
    password = st.text_input("Choose Password", type="password")
    role = st.selectbox("Role", ["user", "admin"])
    if st.button("Sign Up"):
        try:
            add_user(username, password, role)
            st.success("User created! You can now login.")
        except Exception as e:
            st.error(f"Error: {e}")
