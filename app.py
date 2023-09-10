import os
import json
import ee

# Get the environment variable or default to an empty string
service_account_key_str = os.environ.get('GEE_SERVICE_ACCOUNT_KEY', '')

# Check if the string is not empty before trying to load JSON
if service_account_key_str:
    service_account_key = json.loads(service_account_key_str)
    # Use the service account for authentication
    credentials = ee.ServiceAccountCredentials(email=service_account_key['client_email'], key_data=service_account_key['private_key'])
    ee.Initialize(credentials)
else:
    print("GEE_SERVICE_ACCOUNT_KEY is not set!")
    service_account_key = {}

# import streamlit as st
# import os
# import json
# import ee

# # Read the service account key from the environment variable
# service_account_key = json.loads(os.environ.get('GEE_SERVICE_ACCOUNT_KEY'))

# # Use the service account for authentication
# credentials = ee.ServiceAccountCredentials(email=service_account_key['client_email'], key_data=service_account_key['private_key'])
# ee.Initialize(credentials)

st.title("Visualizing Landsat Data with Earth Engine and Streamlit")
# Define a function to visualize Landsat data
def visualize_landsat_data(latitude, longitude):
    # Define a region of interest
    roi = ee.Geometry.Point([longitude, latitude])

    # Fetch a Landsat image
    image = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR') \
        .filterBounds(roi) \
        .first()

    # Define visualization parameters
    vis_params = {
        'min': 0,
        'max': 3000,
        'bands': ['B4', 'B3', 'B2']  # RGB
    }

    # Generate a URL for the image
    url = image.getThumbUrl(vis_params)

    return url

# Get user input for latitude and longitude
latitude = st.number_input("Enter Latitude", value=37.7749)  # Default to San Francisco
longitude = st.number_input("Enter Longitude", value=-122.4194)  # Default to San Francisco

# Fetch and display the Landsat image
if st.button("Show Landsat Data"):
    landsat_url = visualize_landsat_data(latitude, longitude)
    st.image(landsat_url, caption="Landsat Image", use_column_width=True)
