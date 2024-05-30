import streamlit as st
from PIL import Image
from pathlib import Path

# Set the page config
st.set_page_config(
    page_title="Real Estate Application Pune",
    page_icon="🏠",
    layout="wide",
)

    # Page title and custom CSS
st.markdown("""
<style>
.title {
    color: #1f77b4;
    font-size: 36px;
    text-align: center;
}
.header {
    color: #E37546;
    font-size: 24px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)
# Title of the application
st.title("🏠 REAL ESTATE APPLICATION PUNE")
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

# Navigation buttons
# st.sidebar.title("Navigation")


# Main content based on selection

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

# Add the remaining sections

# Run the Streamlit app
if __name__ == "__main__":
    st.write("")

