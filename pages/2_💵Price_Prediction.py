import streamlit as st
import pickle
import pandas as pd
import numpy as np
from PIL import Image
from pathlib import Path

# Set page configuration
st.set_page_config(page_title="Real Estate Price Prediction", page_icon="🏡")

# Load data and model
path_1 = Path('datasets/page_1/df.pkl')
with open(path_1, 'rb') as file:
    df = pickle.load(file)


path_2 = Path('datasets/page_1/xgbmodel.pkl')
with open(path_2, 'rb') as file:
    pipeline = pickle.load(file)

# Custom CSS
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
    color: black; /* Button text color */
    padding: 12px 20px;
    margin: 10px 0;
    border: 1px solid white; /* Button border */
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}
.stButton>button:hover {
    background-color: #45a049;
    color: white; /* Hover text color */
}
.stButton>button:active {
    border: 1px solid #4CAF50; /* Active button border color */
}

</style>
"""

# Inject custom CSS
st.markdown(css, unsafe_allow_html=True)

# Sidebar
st.sidebar.write("""<span style='color: #ffff33 ;'>Please click the down arrow above to view all pages.</span>""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.header("Model Information")
st.sidebar.write("""
- **Model Accuracy:** 93.57% (R² Score)
- **Mean Absolute Error:** 0.17
- **Disclaimer:** You can cross-check the prices from the [99acres website](https://www.99acres.com).""")

# Header
st.title('🏡 Real Estate Price Prediction')

image_path = Path('datasets/page_1/images.jpg')
image = Image.open(image_path)
resized_image = image.resize((1000, 450))  # Set the desired width and height

# Display the resized image
st.image(resized_image, use_column_width=True)
st.markdown("---")


# Guidelines
st.markdown("""
<div class='info'>
    <strong>Guidelines:</strong>
    <ul>
        <li>Fill in all the property details accurately.</li>
        <li>If property is under construction or information related to any variable is not mentioned, select "Not Known" if this option is available.</li>
        <li>Select options from the dropdown menus for categorical inputs.</li>
        <li>For numerical inputs, use the provided fields to enter values.</li>
        <li>For columns Pooja room and Storage room '1' means present and '0' means not present.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
st.markdown("---")
st.header('Enter Property Details')
# Location
with st.expander("Location"):
    location = st.selectbox('Location', sorted(df['location'].unique().tolist()), help="Select the location of the property")

# Property Details
with st.expander("Property Details"):
    bedrooms = float(st.selectbox('Number of Bedrooms', sorted(df['bedrooms'].unique().tolist()), help="Select the number of bedrooms"))
    bathrooms = float(st.selectbox('Number of Bathrooms', sorted(df['bathrooms'].unique().tolist()), help="Select the number of bathrooms"))
    balconies = st.selectbox('Number of Balconies', sorted(df['balconies'].unique().tolist()), help="Select the number of balconies")
    age_of_property = st.selectbox('Age of Property', sorted(df['age_of_property'].unique().tolist()), help="Select the age of the property")
    built_up_area = st.number_input('Built-up Area (sq. ft)', value=1000, step=100, help="Enter the built-up area in square feet")

# Amenities
with st.expander("Amenities"):
    storage_room = float(st.selectbox('Servant Room', [0.0, 1.0], help="Select if there is a servant room (1 for Yes, 0 for No)"))
    pooja_room = float(st.selectbox('Pooja Room', [0.0, 1.0], help="Select if there is a pooja room (1 for Yes, 0 for No)"))
    furnishing_status = st.selectbox('Furnishing Type', ['Not Known'] + sorted(df['furnishing_status'].unique().tolist()), help="Select the furnishing status")
    parking_space = st.selectbox('Parking Type', ['Not Known'] + sorted(df['parking_space'].unique().tolist()), help="Select the type of parking space")
    flooring_type = st.selectbox('Flooring Type', ['Not Known'] + sorted(df['flooring_type'].unique().tolist()), help="Select the type of flooring")
    luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()), help="Select the luxury category")
    floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()), help="Select the floor category")

# Prediction
button_placeholder = st.empty()
prediction_button = button_placeholder.button('Predict')

if prediction_button:
    data = [[bedrooms, bathrooms, balconies, age_of_property, furnishing_status, flooring_type, parking_space,
             built_up_area, storage_room, pooja_room, location, floor_category, luxury_category]]
    columns = ['bedrooms', 'bathrooms', 'balconies', 'age_of_property', 'furnishing_status',
               'flooring_type', 'parking_space', 'built_up_area',
               'storage_room', 'pooja_room', 'location', 'floor_category',
               'luxury_category']

    one_df = pd.DataFrame(data, columns=columns)
    base_price = np.exp(pipeline.predict(one_df))[0]

    if base_price < 1:
        base_price = round(base_price * 100, 2)
        price = "{:.2f}".format(base_price)
        st.markdown("<p class='success' style='font-size: 24px; color: #4CAF50'>The price of the flat is approximately <span style='color: #E6E6E6'>{}</span> <span style='color: #4CAF50'>Lakhs</span></p>".format(price), unsafe_allow_html=True)
    else:
        base_price = round(base_price , 2)
        price = "{:.2f}".format(base_price)
        st.markdown("<p class='success' style='font-size: 24px; color: #4CAF50'>The price of the flat is approximately <span style='color: #E6E6E6'>{}</span> <span style='color: #4CAF50'>Crores</span></p>".format(price), unsafe_allow_html=True)
    
    # Add the 'price' column at the first position
    one_df.insert(0, 'price', price)

    # Display user inputs as DataFrame
    st.markdown("<p class='success' style='font-size: 26px; color: #F0E199'>User Inputs</p>", unsafe_allow_html=True)
    st.dataframe(one_df)

# Reset button

reset_placeholder = st.empty()
reset_button = reset_placeholder.button('↺ Reset', help="Reset")

# Apply custom CSS directly to the reset button
reset_css = """
<style>
.reset-button {
    background-color: #FFFFFF; /* Button background color */
    color: #4CAF50; /* Button text color */
    border: 1px solid #4CAF50; /* Button border */
    border-radius: 50%; /* Make button circular */
    width: 30px; /* Button width */
    height: 30px; /* Button height */
    padding: 0; /* Remove padding */
    display: flex; /* Use flexbox for alignment */
    justify-content: center; /* Center content horizontally */
    align-items: center; /* Center content vertically */
    margin-left: 10px; /* Add margin to separate from other buttons */
}

</style>
"""

# Inject custom CSS for the reset button
st.markdown(reset_css, unsafe_allow_html=True)

if reset_button:
    # Reset all inputs
    location = None
    bedrooms = None
    bathrooms = None
    balconies = None
    age_of_property = None
    built_up_area = 1000
    storage_room = None
    pooja_room = None
    furnishing_status = None
    parking_space = None
    flooring_type = None
    luxury_category = None
    floor_category = None
