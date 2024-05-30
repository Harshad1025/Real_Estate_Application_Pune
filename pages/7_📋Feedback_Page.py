import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import os


import yaml


import yaml

# Load configuration file
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)



# Access sensitive information
HOST_PASSWORD = config.get("HOST_PASSWORD")


# Define the path to the SQLite database file
DB_FILE = Path("datasets/page_5/feedback.db").resolve()

# Function to create a connection to the SQLite database
def create_connection():
    return sqlite3.connect(DB_FILE)

# Function to create the feedback table if it doesn't exist
def create_feedback_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS feedback 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, feedback TEXT, rating INTEGER)''')
    conn.commit()
    conn.close()

# Function to load feedback from the SQLite database

def load_feedback():
    create_feedback_table()  # Ensure the table exists
    conn = create_connection()
    feedback_df = pd.read_sql_query("SELECT id, name, feedback, rating FROM feedback", conn)
    conn.close()
    return feedback_df


def delete_feedback(feedback_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute("DELETE FROM feedback WHERE id=?", (feedback_id,))
    conn.commit()
    conn.close()
# Streamlit page to display feedback
def main():
    # Custom CSS styles
    st.markdown("""
        <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f2f6;
            color: #333;
        }
        .stApp {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
        }
        h1 {
            color: #ff8c1a;       
        }
        h2, h3 {
            color: #3399ff;
        }
        .header {
            color: #3399ff;
        }
        .feedback {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
            background-color: #f9f9f9;
        }
        .feedback .name {
            font-weight: bold;
            color: #4CAF50;
            font-size: 20px;
        }
        .feedback .rating {
            color: #ffb400;
        }
        .feedback .comment {
            color: #000000;
            font-size: 18px;
        }
        .emoji {
            font-size: 24px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📋 Feedback Page")

    st.markdown('<h2>💬 All Feedback</h2>', unsafe_allow_html=True)
    feedback_df = load_feedback()

    if feedback_df.empty:
        st.write("No feedback available yet. 😔")
    else:
        st.write("Here is the feedback received so far:")
        # Authentication for deletion
        st.sidebar.subheader("Admin Login")
        password = st.sidebar.text_input("Enter password", type="password")
        if password == HOST_PASSWORD:
            is_host = True
            st.sidebar.success("Logged in as host")
        else:
            is_host = False

        if not is_host and password != "":
            # Show message for unauthorized access only if password is not empty and doesn't match
            st.sidebar.error("Access denied. You are not authorized to view this section.")


        # Display each feedback entry with custom styling and delete button for host
        for index, row in feedback_df.iterrows():
            feedback_id = row['id']
            name = row['name']
            rating = row['rating']
            feedback = row['feedback']
            st.markdown(f"""
                <div class="feedback">
                    <div class="name">👤 {name}</div>
                    <div class="rating">⭐ {rating}</div>
                    <div class="comment">{feedback}</div>
                </div>
            """, unsafe_allow_html=True)

            if is_host:
                if st.button(f"Delete", key=f"delete_{feedback_id}"):
                    delete_feedback(feedback_id)
                    st.experimental_rerun()

        st.sidebar.markdown("---")
    
    # Thank you message
    st.markdown("""
        <div class="thank-you">
            <h3>🙏 Thank you for visiting our application! 🎉</h3>
            <p>We appreciate your valuable time and feedback. 😊</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <style>
    .thank-you {
        background-color: #91f29e;
        color: #333;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        font-family: 'Arial', sans-serif;
        margin-top: 20px;
    }
    .thank-you h3 {
        color: #3399ff;
        font-size: 24px;
        margin-bottom: 10px;
    }
    .thank-you p {
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)



if __name__ == "__main__":
    main()
