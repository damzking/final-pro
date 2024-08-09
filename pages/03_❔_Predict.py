import streamlit as st
import joblib
import pandas as pd
import os
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import requests

# Set up the page configuration
st.set_page_config(
    page_title="Ride hailing ETA Prediction (in seconds)",
    layout="wide",
    initial_sidebar_state="expanded",
)

api_url = 'http://127.0.0.1:8000'

# Load the authentication configuration
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# Check authentication status
if st.session_state['authentication_status']:
    # Logout button
    authenticator.logout(location='sidebar')
    
    # Title and model selection
    st.title(":rainbow[Ride ETA Prediction Parameters]")
    col1, col2 = st.columns(2)

    # Initialize session state variables
    if 'prediction' not in st.session_state:
        st.session_state['prediction'] = None

    with col1:
        st.selectbox('Select Model', options=['GB_Model', 'XGB_Model'], key='model_name')
        model_name = st.session_state['model_name']

    # Function to display the input form
    def show_form():
        with st.form('enter_features'):
            col1, col2 = st.columns(2)
            with col1:
                st.number_input("Enter Latitude of your pickup location", min_value=0.0, max_value=10000.0, key='Origin_lat')
                st.number_input("Enter Longitude of your pickup location", min_value=0.0, max_value=10000.0, key='Origin_lon')
                st.number_input("Enter Latitude of your destination", min_value=0.0, max_value=10000.0, key='Destination_lat')        
                st.number_input("Enter Longitude of your destination", min_value=0.0, max_value=10000.0, key='Destination_lon')
                st.number_input("Enter Trip distance in meters", min_value=0, max_value=1000000, key='Trip_distance')
                st.number_input('Enter the year', min_value=2000, max_value=3000, key='Year')
            with col2:
                st.number_input('Enter the month', min_value=1, max_value=12, key='Month')
                st.number_input("Enter the day", min_value=1, max_value=31, key='Day')
                st.number_input("Enter the hour", min_value=0, max_value=23, key='Hour')
                st.number_input("Enter the minute", min_value=0, max_value=59, key='Minute')
            st.form_submit_button(':green[Predict Estimated Time of Arrival]', on_click=make_prediction)

    # Function to make prediction using the API
    def make_prediction():
        data = {
            'Origin_lat': st.session_state['Origin_lat'],
            'Origin_lon': st.session_state['Origin_lon'],
            'Destination_lat': st.session_state['Destination_lat'],
            'Destination_lon': st.session_state['Destination_lon'],
            'Trip_distance': st.session_state['Trip_distance'],
            'Year': st.session_state['Year'],
            'Month': st.session_state['Month'],
            'Day': st.session_state['Day'],
            'Hour': st.session_state['Hour'],
            'Minute': st.session_state['Minute']
        }
        # Send POST request to the API
        response = requests.post(f'{api_url}/predict/{model_name}', json=data)
        
        # Parse response data
        response_data = response.json()
        st.session_state['prediction'] = response_data['prediction']
        st.session_state['probability'] = response_data.get('probability', 'N/A')

    # Display form and prediction results
    st.header('Predict Estimated Time of Arrival')
    show_form()
    
    final_prediction = st.session_state.get('prediction')
    if final_prediction is None:
        st.write('### Prediction will show here')
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"### The Estimated Time of Arrival is: :red[{final_prediction} seconds]")

else:
    # Display only the login prompt if not authenticated
    st.info('Please log in to access the app.')
