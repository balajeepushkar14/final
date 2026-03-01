import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from auth import login, signup
from database import add_mental_health_entry, get_user_entries, get_all_users

# Initialize session state
if 'username' not in st.session_state:
    st.session_state['username'] = None
    st.session_state['role'] = None

st.title("Mental Health Dashboard App")

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

# Authentication
if choice == "Login":
    login()
elif choice == "Sign Up":
    signup()

# User Dashboard
if st.session_state['username'] and st.session_state['role'] == 'user':
    st.subheader(f"Welcome {st.session_state['username']}")
    
    # Add mental health entry
    st.markdown("### Add Daily Entry")
    with st.form("entry_form"):
        date = st.date_input("Date", datetime.today())
        stress = st.slider("Stress Level (0-10)", 0, 10, 5)
        mood = st.slider("Mood Level (0-10)", 0, 10, 5)
        anxiety = st.slider("Anxiety Level (0-10)", 0, 10, 5)
        submitted = st.form_submit_button("Submit")
        if submitted:
            add_mental_health_entry(st.session_state['username'], str(date), stress, mood, anxiety)
            st.success("Entry added successfully!")

    # Show historical data
    st.markdown("### Your Mental Health History")
    data = get_user_entries(st.session_state['username'])
    if data:
        df = pd.DataFrame(data, columns=["Date", "Stress", "Mood", "Anxiety"])
        st.dataframe(df)

        # Line chart
        st.line_chart(df.set_index("Date"))
    else:
        st.info("No entries yet. Start adding today!")

# Admin Dashboard
if st.session_state['username'] and st.session_state['role'] == 'admin':
    st.subheader(f"Welcome Admin {st.session_state['username']}")
    st.markdown("### All Users")
    users = get_all_users()
    df_users = pd.DataFrame(users, columns=["ID", "Username", "Role"])
    st.dataframe(df_users)

    st.markdown("### All User Entries")
    all_entries = []
    for user in df_users['Username']:
        entries = get_user_entries(user)
        for e in entries:
            all_entries.append([user, *e])
    if all_entries:
        df_all = pd.DataFrame(all_entries, columns=["Username", "Date", "Stress", "Mood", "Anxiety"])
        st.dataframe(df_all)
    else:
        st.info("No entries yet.")
