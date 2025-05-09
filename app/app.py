# /app/app.py

import streamlit as st
import sqlite3
import os
import datetime
from dotenv import load_dotenv
import os
from services.openai_service import summarize_user_log


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# 2. Main entry point of the app
if __name__ == "__main__":
    # Example daily log
    user_log = "Today I woke up early, went for a run, finished my work tasks, but forgot to journal."

    # Use OpenAI to summarize the log
    ai_summary = summarize_user_log(user_log)

    # Output the AI summary
    print("\n=== AI Summary of Your Day ===")
    print(ai_summary)

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

# Create a new table to track when habits are completed
c.execute('''
    CREATE TABLE IF NOT EXISTS habit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        log_date DATE DEFAULT (date('now')),
        FOREIGN KEY (habit_id) REFERENCES habits (id)
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

# --- Daily Summary Section ---

st.subheader("📊 Daily Summary")

today = datetime.date.today()

# Total number of habits
c.execute("SELECT COUNT(*) FROM habits")
total_habits = c.fetchone()[0]

# Total number of habits completed today
c.execute('''
    SELECT COUNT(DISTINCT habit_id) FROM habit_logs
    WHERE log_date = ?
''', (today,))
completed_habits = c.fetchone()[0]

# Calculate success rate
if total_habits > 0:
    success_rate = (completed_habits / total_habits) * 100
else:
    success_rate = 0

# Display results
st.metric(label="Total Habits", value=total_habits)
st.metric(label="Completed Today", value=completed_habits)
st.metric(label="Success Rate", value=f"{success_rate:.0f}%")


# --- Show current habits with completion checkboxes ---
if habits:
    today = datetime.date.today()

    for habit in habits:
        habit_name = habit[0]
        created_at = habit[1]
        
        # Check if the habit was completed today
        c.execute('''
            SELECT id FROM habits WHERE habit_name = ?
        ''', (habit_name,))
        habit_id = c.fetchone()[0]

        c.execute('''
            SELECT 1 FROM habit_logs
            WHERE habit_id = ?
            AND log_date = ?
        ''', (habit_id, today))
        completed_today = c.fetchone() is not None

        # Create a checkbox, default ticked if already completed
        completed = st.checkbox(f"{habit_name}", key=habit_name, value=completed_today)

        if completed and not completed_today:
            # Insert a log if it wasn't already completed today
            c.execute('''
                INSERT INTO habit_logs (habit_id, log_date) VALUES (?, ?)
            ''', (habit_id, today))
            conn.commit()
            st.success(f"Marked {habit_name} as completed today!")
            st.rerun()

        elif not completed and completed_today:
            # Delete the log if it was previously completed but now unticked
            c.execute('''
                DELETE FROM habit_logs
                WHERE habit_id = ?
                AND log_date = ?
            ''', (habit_id, today))
            conn.commit()
            st.warning(f"Unmarked {habit_name} as completed today.")
            st.rerun()

else:
    st.write("No habits added yet.")



# --- Close DB connection at end ---
conn.close()
