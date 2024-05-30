import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path




st.set_page_config(page_title="Plotting Demo")


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
.selectbox-label {
    font-size: 18px;
    color: #4CAF50;
}
.selectbox-options {
    background-color: #f0f0f5;
    color: #333333;
    border-radius: 4px;
    padding: 8px 12px;
    font-size: 16px;
}
.selectbox-arrow::after {
    border-color: #4CAF50;
}
.reset-button {
    background-color: #FFFFFF;
    color: #4CAF50;
    border: 1px solid #4CAF50;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    padding: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-left: 10px;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)



st.title('🏡 Pune Real Estate Analytics 📊')


image_path = "datasets/page_3/data_analysis_image.jpg"
image = Image.open(image_path)
resized_image = image.resize((1000, 500))  # Set the desired width and height

# Display the resized image
st.image(resized_image, use_column_width=True)
st.markdown("""
Welcome to the Pune Real Estate Analytics Dashboard! Here you can explore various insights and visualizations about real estate prices, locations, and features in Pune. Use the interactive charts and maps to gain a deeper understanding of the market trends. Let's dive in! 🌟
""")

path_0 = Path('datasets/page_3/feature_text.pkl')
feature_text = pickle.load(open(path_0,'rb'))



# Load the data
path_1 = 'datasets/page_3/median_agg_map_df.xls'
group_df_median = pd.read_csv(path_1)

path_2 = Path('datasets/page_3/avg_agg_map_df.xls')
group_df_mean = pd.read_csv(path_2)

path_3 = Path('datasets/page_3/analystics_module_data.xls')
new_df = pd.read_csv(path_3)

# Rename columns for consistency
group_df_median.columns = ['Location', 'Price', 'Price Per Sq.Ft.', 'Built Up Area', 'Latitude', 'Longitude']
group_df_mean.columns = ['Location', 'Price', 'Price Per Sq.Ft.', 'Built Up Area', 'Latitude', 'Longitude']


st.markdown("---")
# Streamlit app
st.markdown("<h2 style='text-align: center; color: #00FA71;'>📍 Location Price per Sqft Geomap</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='info'>
    <strong>Guidelines:</strong>
    <ul>
        <li>Select 'Mean' or 'Median' to visualize the average or median price per sqft for different locations on the map.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# In the main Streamlit script
agg_method = st.radio(
    "Choose the aggregation method:",
    ('Mean', 'Median'),
    key='aggregation_method_streamlit'  
)


# if st.button('Compare Both'):
#     open_dash_app()

if agg_method == 'Mean':
    fig_mean = px.scatter_mapbox(group_df_mean, lat="Latitude", lon="Longitude", color="Price Per Sq.Ft.", size='Built Up Area',
                                 color_continuous_scale=px.colors.cyclical.IceFire, zoom=9.7,
                                 mapbox_style="open-street-map", width=1600, height=550, hover_name='Location',
                                 hover_data={'Price': True})

    fig_mean.update_traces(hovertemplate=
                           "<b>Location:</b> %{hovertext}<br>"
                           "<b>Price per Sq.Ft.:</b> ₹%{marker.color:.2f}<br>"
                           "<b>Built Up Area:</b> %{marker.size:,.2f} sq.ft.<br>"
                           "<b>Price:</b> ₹%{customdata[0]:,.2f} Crore<br><extra></extra>")

    st.plotly_chart(fig_mean, use_container_width=True)

elif agg_method == 'Median':
    fig_median = px.scatter_mapbox(group_df_median, lat="Latitude", lon="Longitude", color="Price Per Sq.Ft.", size='Built Up Area',
                                   color_continuous_scale=px.colors.cyclical.IceFire, zoom=9.7,
                                   mapbox_style="open-street-map", width=1600, height=550, hover_name='Location',
                                   hover_data={'Price': True})

    fig_median.update_traces(hovertemplate=
                             "<b>Location:</b> %{hovertext}<br>"
                             "<b>Price per Sq.Ft.:</b> ₹%{marker.color:.2f}<br>"
                             "<b>Built Up Area:</b> %{marker.size:,.2f} sq.ft.<br>"
                             "<b>Price:</b> ₹%{customdata[0]:,.2f} Crore<br><extra></extra>")

    st.plotly_chart(fig_median, use_container_width=True)
st.markdown("---")

st.markdown("<h2 style='text-align: center; color: #00FA71;'>📏 Area Vs Price</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='info'>
    <strong>Guidelines:</strong>
    <ul>
        <li>Explore the relationship between the built-up area and the price of properties in Pune.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

fig = px.scatter(new_df, x="built_up_area", y="price", color="bedrooms", title="Area Vs Price")
fig.update_layout(
    width=900,
    height=600,
    xaxis_title="Built-up Area",
    yaxis_title="Price (Crores)",
    hovermode="closest",
)

fig.update_yaxes(
    tickprefix="₹",
    tickformat=",.2f",
    ticksuffix=" Crore",
)

fig.update_traces(hovertemplate=
                  "<b>Built-up Area:</b> %{x} sq.ft.<br>"
                  "<b>Price:</b> ₹%{y:.2f} Crore<br>"
                  "<b>Bedrooms:</b> %{marker.color}<br><extra></extra>")

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.markdown("<h2 style='text-align: center; color: #00FA71;'>🏠 BHK Pie Chart</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='info'>
    <strong>Guidelines:</strong>
    <ul>
        <li>View the distribution of properties based on the number of bedrooms.</li>
        <li>Choose a location to see the distribution specific to that area.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

location_options = new_df['location'].unique().tolist()
location_options.insert(0, 'overall')

selected_location = st.selectbox('Select Location', location_options)

if selected_location == 'overall':
    fig2 = px.pie(new_df, names='bedrooms',
                  title='Distribution of Bedrooms',
                  color_discrete_sequence=px.colors.qualitative.Pastel)
else:
    fig2 = px.pie(new_df[new_df['location'] == selected_location],
                  names='bedrooms',
                  title=f'Distribution of Bedrooms in {selected_location}',
                  color_discrete_sequence=px.colors.qualitative.Pastel)

fig2.update_traces(textposition='inside', textinfo='percent+label', hoverinfo='label+percent+name', pull=[0.02] * len(new_df['bedrooms']))

fig2.update_layout(
    font=dict(
        family="Arial, sans-serif",
        size=13.5
    ),
    legend=dict(
        title=None,
        font=dict(
            family="Arial, sans-serif",
            size=10
        )
    )
)

st.plotly_chart(fig2, use_container_width=True)
st.markdown("---")

st.markdown("<h2 style='text-align: center; color: #00FA71;'>🏢 Side by Side BHK Price Comparison</h2>", unsafe_allow_html=True)

st.markdown("""
<div class='info'>
    <strong>Guidelines:</strong>
    <ul>
        <li>Compare the price range of properties based on the number of bedrooms.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

fig = px.box(new_df[new_df['bedrooms'] <= 4], x='bedrooms', y='price', title='BHK Price Range')

fig.update_xaxes(title_text='Number of Bedrooms', tickfont=dict(size=12))
fig.update_yaxes(title_text='Price', tickfont=dict(size=12))

fig.update_traces(hovertemplate=
                  "<b>Bedrooms:</b> %{x}<br>"
                  "<b>Price:</b> ₹%{y:.2f} Crore<br><extra></extra>",
                  marker=dict(color='rgba(0, 123, 255, 0.6)', line=dict(color='rgba(0, 123, 255, 1.0)', width=1)))

fig.update_layout(
    font=dict(
        family="Arial",
        size=14,
        color="white"
    ),
    paper_bgcolor='rgba(0, 0, 0, 0.8)',
    plot_bgcolor='rgba(0, 0, 0, 0.8)',
    title_font=dict(size=20, color='white'),
    legend=dict(
        title_font=dict(size=16),
        font=dict(size=12, color='white')
    ),
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.markdown("<h2 style='text-align: center; color: #00FA71;'>🔍 Features Wordcloud</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='info'>
    <strong>Guidelines:</strong>
    <ul>
        <li>Explore the most common features mentioned in property listings through a word cloud.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

wordcloud = WordCloud(width=800, height=600,
                      background_color='black',
                      stopwords=set(['s']),
                      min_font_size=10).generate(feature_text)

fig, ax = plt.subplots(figsize=(8, 8), facecolor=None)
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
plt.tight_layout(pad=0)

st.pyplot(fig)
st.markdown("---")

st.markdown("<h2 style='text-align: center; color: #00FA71;'>📊 Feature Wise Price Comparison</h2>", unsafe_allow_html=True)
st.markdown("""
<div class='info'>
    <strong>Guidelines:</strong>
    <ul>
        <li>View the average or median price of properties based on different features.</li>
        <li>Select a categorical variable and calculation type ('Mean' or 'Median') to see the corresponding price comparison.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
column_display_names = {
    'bedrooms': 'Bedrooms',
    'bathrooms': 'Bathrooms',
    'balconies': 'Balconies',
    'facing': 'Facing',
    'age_of_property': 'Age of Property',
    'furnishing_status': 'Furnishing Status',
    'flooring_type': 'Flooring Type',
    'parking_space': 'Parking Space',
    'study_room': 'Study Room',
    'servant_room': 'Servant Room',
    'storage_room': 'Storage Room',
    'pooja_room': 'Pooja Room',
    'others': 'Others',
    'location': 'Location',
    'floor_category': 'Floor Category',
    'luxury_category': 'Luxury Category'
}

selected_option = st.selectbox("Select a categorical variable", ['Bedrooms', 'Bathrooms', 'Balconies', 'Facing',
                                                                'Age of Property', 'Furnishing Status', 'Flooring Type',
                                                                'Parking Space', 'Study Room', 'Servant Room',
                                                                'Storage Room', 'Pooja Room', 'Others', 'Location',
                                                                'Floor Category', 'Luxury Category'])

calculation_type = st.radio("Select calculation type", ['Mean', 'Median'])

selected_column = [key for key, value in column_display_names.items() if value == selected_option][0]

if calculation_type == 'Mean':
    avg_price_df = new_df.groupby(selected_column)['price'].mean().reset_index()
else:
    avg_price_df = new_df.groupby(selected_column)['price'].median().reset_index()

title = f"{calculation_type} Price by {selected_option}"
fig = px.bar(avg_price_df, x=selected_column, y='price', title=title,
             labels={'price': f'{calculation_type} Price', selected_column: selected_option})

fig.update_layout(
    font=dict(
        family="Arial",
        size=14,
        color="white"
    ),
    paper_bgcolor='rgba(0, 0, 0, 0.8)',
    plot_bgcolor='rgba(0, 0, 0, 0.8)',
    title_font=dict(size=20, color='white'),
    xaxis=dict(tickfont=dict(size=12)),
    yaxis=dict(tickfont=dict(size=12)),
)

hover_template = f"<b>{selected_option}:</b> %{{x}}<br>" + "<b>Price:</b> ₹%{y:.2f} Crore<br><extra></extra>"
fig.update_traces(hovertemplate=hover_template)
st.markdown("---")
st.plotly_chart(fig, use_container_width=True)


st.markdown("---")

video_path = Path("datasets/page_3/data_analysis.mp4")
video_bytes = video_path.read_bytes()

# Display the video using st.video()
st.video(video_bytes)
