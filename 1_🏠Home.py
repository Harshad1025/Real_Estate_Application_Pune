import streamlit as st
from PIL import Image
from pathlib import Path
import sqlite3
import pandas as pd

# Set the page config
st.set_page_config(
    page_title="Real Estate Application Pune",
    page_icon="🏠",
    layout="wide",
)



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
    feedback_df = pd.read_sql_query("SELECT name, feedback, rating FROM feedback", conn)
    conn.close()
    return feedback_df

# Function to calculate average rating and count reviews
def calculate_feedback_stats(feedback_df):
    avg_rating = feedback_df['rating'].mean()
    review_count = feedback_df.shape[0]
    return avg_rating, review_count


    # Page title and custom CSS
st.markdown("""
<style>
.title {
    color: #1f77b4;
    font-size: 36px;
    text-align: center;
}
.header {
    color: #00000;
    font-size: 24px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)


feedback_df = load_feedback()

# Calculate average rating and review count
avg_rating, review_count = calculate_feedback_stats(feedback_df)

# Display average rating and review count with styling
st.sidebar.write("""<span style='color: #ffff33 ;'>Please click the down arrow above to view all pages.</span>""", unsafe_allow_html=True)

st.sidebar.markdown("---")
background_color = "#f0f0f0"
text_color = "#333333"

# Define CSS styles
css_style_ = f"""
    <style>
        .sidebar-content {{
            background-color: {background_color};
            color: {text_color};
            padding: 15px;
            border-radius: 8px;
        }}
    </style>
"""

# Markdown content with CSS styles
markdown_content = f"""
<div class="sidebar-content">
    <div style='text-align: center; padding: 5px; font-size: 18px;'>
        <span style='font-size: 25px;'>🌟</span><br>
        <strong>Average Rating:</strong> {avg_rating:.2f}<br>
        <span style='font-size: 25px;'>📝</span><br>
        <strong>Total Reviews:</strong> {review_count}
    </div>
</div>
"""


# Render markdown content with CSS styles in the sidebar
st.sidebar.markdown(css_style_, unsafe_allow_html=True)
st.sidebar.markdown(markdown_content, unsafe_allow_html=True)
# Title of the application
# Set title



# Set title with CSS styles
st.markdown("""
    <h1 style='
        color: #33ff33; /* Light gray text color */
        font-family: Arial, sans-serif; /* Font family */
        font-size: 38px; /* Font size */
        font-weight: bold; /* Make text bold */
        text-shadow: 2px 2px 4px rgba(255, 255, 0, 0.3); /* Add shadow with faint yellow color */
        text-align: center; /* Center the title */
    '>
        🏠 REAL ESTATE APPLICATION PUNE
    </h1>
""", unsafe_allow_html=True)



         
def main():



        
    image_path = Path("datasets/home_page/image_1.jpg")
    image = Image.open(image_path)
    resized_image = image.resize((900, 450))  # Set the desired width and height

    # Display the resized image
    st.image(resized_image, use_column_width=True)

    # Introduction
    st.markdown("""<h1 class='title'> Welcome to Real Estate Application Pune!</h1>""", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 18px; font-weight: bold; color: #F8E85E;'>This application is built for educational purposes and utilizes real-time data scraped from the 99 Acres website.</p>", unsafe_allow_html=True)


    # Divider line
    st.markdown("---")

        # Home Page Content
    st.markdown("""
    ### Explore the world of real estate in Pune!

    This application provides a variety of tools and insights to help you navigate the Pune real estate market.

    - **Price Prediction**: Predict future property prices.
    - **Property Recommendation**: Get personalized property recommendations.
    - **Analytics**: Analyze market trends and visualize data.
    - **Dashboard**: Access detailed dashboards with various metrics and visualizations.
    - **Final Page**: View the final summary and insights.
    """)

        # Divider line
    st.markdown("---")

        # Guidelines Section
    st.markdown("### 📜 Guidelines for Using the Application")
    st.markdown("""
    Follow these guidelines to make the most out of our real estate application:
    - Use the navigation panel to switch between different sections.
    - Ensure accurate inputs for price predictions.
    - Utilize filters and options for customized views.
    - For property recommendations, choose from four types: property info-based, facilities, nearby location, and combined all.
    - Explore the analytical module for maps and visualizations.
    - Provide feedback and rating on the final page.
    """)


if __name__ == "__main__":
    main()

