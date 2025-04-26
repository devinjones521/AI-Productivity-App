# /app/app.py

import streamlit as st
import sqlite3
import os

# --- App title ---
st.title("🧠 Productivity App")

# --- Database setup ---
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'productivity.db')

# Create connection
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create a simple table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

# --- Simple UI ---
st.subheader("Welcome!")
st.write("Your productivity journey starts here. 🚀")

# --- Add new habit form ---
st.subheader("Add a New Habit")

with st.form(key='habit_form'):
    new_habit = st.text_input("Enter a new habit:")
    submit_button = st.form_submit_button(label='Add Habit')

    if submit_button and new_habit.strip() != "":
        # Insert the new habit into the database
        c.execute('INSERT INTO habits (habit_name) VALUES (?)', (new_habit.strip(),))
        conn.commit()
        st.success(f"Added habit: {new_habit}")
        st.rerun() # Refresh the page to show updated habits


# Show all habits in database
st.subheader("Current Habits:")

# Fetch habits
c.execute("SELECT habit_name, created_at FROM habits")
habits = c.fetchall()

if habits:
    for habit in habits:
        st.write(f"- {habit[0]} (added {habit[1]})")
else:
    st.write("No habits added yet.")

# --- Close DB connection at end ---
conn.close()
