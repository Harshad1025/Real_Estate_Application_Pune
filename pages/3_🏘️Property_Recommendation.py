import streamlit as st
import pandas as pd
from PIL import Image
from pathlib import Path

# Load data
path_1 = Path('datasets/page_2/Recomendation_system_final_data.xls')
joined_df = pd.read_csv(path_1)

path_2 = Path('datasets/page_2/cosine_sim_by_near_by_locations.pkl')
cosine_sim_by_near_by_locations = pd.read_pickle(path_2)

path_3 = Path('datasets/page_2/cosine_sim_facility_based.pkl')
cosine_sim_facility_based = pd.read_pickle(path_3)

path_4 = Path('datasets/page_2/cosine_sim_property_inof_based.pkl')
cosine_sim_property_inof_based = pd.read_pickle(path_4)

# Unique property list
unique_properties = joined_df['society_name'].unique()
image_path = Path("datasets/page_2/poperty_image2.jpeg")
image = Image.open(image_path)

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

.selectbox-label {
    font-size: 18px;
    color: #4CAF50;
}

.selectbox-options {
    background-color: #f0f0f5; /* Background color */
    color: #333333; /* Text color */
    border-radius: 4px; /* Border radius */
    padding: 8px 12px; /* Padding */
    font-size: 16px; /* Font size */
}

.selectbox-arrow::after {
    border-color: #4CAF50; /* Arrow color */
}

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

# Inject custom CSS
st.markdown(css, unsafe_allow_html=True)
st.sidebar.write("""<span style='color: #ffff33 ;'>Please click the down arrow above to view all pages.</span>""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.header("Accuracy Verification")

st.sidebar.write("""
- You can verify the accuracy of the recommendation system by comparing the recommended properties with their respective details in the dataframe.
""")

# Recommendation function
def recommend_properties(property_name, option, n=5):
    id = joined_df.index[joined_df['society_name'] == property_name.lower()].tolist()[0]

    if option == "nearby_locations":
        cosine_sim_matrix = cosine_sim_by_near_by_locations
        cosine_sim_weights = [1, 0, 0]
    elif option == "facility_based":
        cosine_sim_matrix = cosine_sim_facility_based
        cosine_sim_weights = [0, 1, 0]
    elif option == "property_info_based":
        cosine_sim_matrix = cosine_sim_property_inof_based
        cosine_sim_weights = [0, 0, 1]
    else:
        cosine_sim_matrix = 0.8 * cosine_sim_property_inof_based + 0.6 * cosine_sim_facility_based + 1 * \
                            cosine_sim_by_near_by_locations
        cosine_sim_weights = [0.8, 0.6, 1]

    sim_scores = list(enumerate(cosine_sim_matrix[id]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:n + 1]
    property_indices = [i[0] for i in sim_scores]

    recommendations_df = pd.DataFrame({
        'PropertyName': joined_df['society_name'].iloc[property_indices],
        'SimilarityScore': [round(t[1] * 100, 2) for t in sim_scores]
    })

    return recommendations_df

# Streamlit UI
def main():
    st.title("🏘️ Property Recommendation")
    resized_image = image.resize((700, 400))  # Set the desired width and height
    st.image(resized_image, use_column_width=True)
    st.markdown("---")
    # Guidelines
    st.markdown("""
    <div class='info'>
        <strong>Guidelines:</strong>
        <ul>
            <li>Select a society name from the dropdown list.</li>
            <li>Choose a recommendation basis from the options provided. There are three types of recommendation systems available:
                <ul>
                    <li><strong>Nearby Locations:</strong> Recommends properties based on similarity to nearby locations.</li>
                    <li><strong>Facility Based:</strong> Recommends properties based on available facilities and amenities.</li>
                    <li><strong>Property Info Based:</strong> Recommends properties based on property-specific information such as type, price, and number of bedrooms.</li>
                </ul>
            </li>
            <li>Click on the "🔍 Recommend" button to get property recommendations.</li>
            <li>You can view details of recommended properties below the recommendations.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    # Convert property names to title case
    unique_properties_title_case = [property_name.title() for property_name in unique_properties]

    # Selectbox for property names
    property_name = st.selectbox("Select Society Name:", unique_properties_title_case, key='society_name',index=1)

    # Selectbox for recommendation basis
    option_mapping = {
        "nearby_locations": "Nearby Locations",
        "facility_based": "Facility Based",
        "property_info_based": "Property Info Based",
        "auto": "Combined"
    }
    option = st.selectbox("Select Recommendation Basis:", list(option_mapping.values()), index=0, key='recommendation_basis')  # Default selection to "Property Info Based"

    option = [key for key, value in option_mapping.items() if value == option][0]
    # Recommend button
    if st.button("🔍 Recommend"):
        recommendations = recommend_properties(property_name, option)
        st.dataframe(recommendations)

        # Display details of recommended properties
        st.subheader("🏠 Details of Recommended Properties:")

        if not recommendations.empty:
            recommended_indices = recommendations.index.tolist()
            if option == "facility_based":
                property_details = joined_df.loc[recommended_indices][
                    ['society_name', 'property_name', 'features', 'link']]
            elif option == "nearby_locations":
                property_details = joined_df.loc[recommended_indices][
                    ['society_name', 'property_name', 'place', 'nearby_locations', 'link']]
            elif option == "property_info_based":
                property_details = joined_df.loc[recommended_indices][
                    ['society_name', 'property_name', 'property_type', 'price', 'bedrooms', 'built_up_area',
                     'bathrooms', 'balconies', 'age_possession', 'furnish_label', 'parking_availability',
                     'luxury_score', 'link']]
            else:  # auto
                property_details = joined_df.loc[recommended_indices][
                    ['society_name', 'place', 'property_name', 'price', 'bedrooms', 'price_per_sqft', 'property_type',
                     'age_possession', 'furnish_label', 'features', 'link']]

            st.dataframe(property_details)

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


if __name__ == "__main__":
    main()
