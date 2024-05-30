import streamlit as st



css = """
<style>
body {
    font-family: 'Arial', sans-serif;
}
h1 {
    color: #1f77b4;
}
h2, h3 {
    color: #E37546;
}
.sidebar .sidebar-content {
    background-color: #f0f0f5;
}
.stButton>button {
    background-color: #4CAF50;
    color: black;
    padding: 12px 20px;
    margin: 10px 0;
    border: 1px solid white;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}
.stButton>button:hover {
    background-color: #45a049;
    color: white;
}
.stButton>button:active {
    border: 1px solid #4CAF50;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)


# Title of the Streamlit app
st.title("🏠 Real Estate Dashboard")

# Introduction
st.markdown("""
## Welcome to the Real Estate Dashboard!

This comprehensive dashboard provides valuable insights into the real estate market in Pune. Explore various metrics, visualizations, and data tables to gain a deeper understanding of property trends and statistics.
""")



st.markdown("""<p style='font-size: 16px ;color: #F8E85E;'>Please wait a moment for the dashboard to load.<br> For better viewing experience, click on the full-screen mode.</p>""", unsafe_allow_html=True)

st.markdown("""

**Navigate to different sections:**
- Overview
- Summary
- Details

""", unsafe_allow_html=True)
st.markdown("---")
# Embed Power BI dashboard using an iframe
st.markdown("""
<iframe title="pune dashboard" width="700" height="447" src="https://app.powerbi.com/view?r=eyJrIjoiN2FiYTgyODQtYmY3Yy00ZGE1LThiZDYtM2Q3NDQ4MmFiMTkyIiwidCI6IjAyNzIxODE4LTY0MTEtNDM1MC1hYjdkLWE4ZWQ5OGMyN2U3NSJ9" frameborder="0" allowFullScreen="true"></iframe>
""", unsafe_allow_html=True)

# Divider line
st.markdown("---")

# Detailed information about the dashboard
st.markdown("""
### 📊 Dashboard Overview

#### **Dashboard 1: Overview**
- **KPIs:**
  - Total number of properties
  - Average price of a property in Pune
  - Median price of a property in Pune
  - Average price per sq ft
  - Median price per sq ft
  - Average built-up area in sq ft
  - Median built-up area in sq ft


- **Visualizations:**
  - Scatter plot: Price vs. Built-up Area
  - Horizontal bar charts:
    - Average price by location
    - Average price by number of balconies
    - Average price by number of bedrooms
    - Average price by parking type
    - Property count by floor number

- **Filters:**
  - Bedrooms
  - Location
  - Furnish status
  - Luxury category

#### **Page 2: Details**
- **Dataset Table:**
  - Detailed property data with filters for:
    - Bedrooms
    - Location
    - Furnish status
    - Luxury category
    - Additional filters (slicers) for:
      - Built-up area
      - Price
      - Price per sq ft

#### **Page 3: Summary**
- **Bedroom-wise Property Summary:**
  - Overview of property metrics segmented by the number of bedrooms
- **Filters:**
  - Parking type
  - Location
  - Furnish status
  - Luxury category

### 📈 Explore the Data

Navigate through the dashboard pages to explore various visualizations and data tables. Use the filters to customize the data views to your preference. This dashboard is designed to provide you with the most relevant and actionable insights into the Pune real estate market.
""")

