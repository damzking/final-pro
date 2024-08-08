import streamlit as st
import joblib
import pandas as pd
import os
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# Set up the page configuration
st.set_page_config(
    page_title='ETA Prediction App',
    page_icon='🚗',
    layout='wide'
)

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

# Load models
@st.cache_resource()
def load_model(model_name):
    return joblib.load(f'./models/{model_name}.joblib')

# Load and select model
def select_model():
    col1, _ = st.columns(2)
    with col1:
        model_name = st.selectbox('Select Model', options=['GB_Model', 'XGB_model'], key='selected_model')

    pipeline = load_model(model_name)
    return pipeline

# Function to make predictions
def make_prediction(pipeline):
    data = {
        'Origin_lat': st.session_state['Origin_lat'],
        'Origin_lon': st.session_state['Origin_lon'],
        'Destination_lat': st.session_state['Destination_lat'],
        'Destination_lon': st.session_state['Destination_lon'],
        'Trip_distance': st.session_state['Trip_distance'],
        'Year': st.session_state['Year'],
        'Day': st.session_state['Day'],
        'Month': st.session_state['Month'],
        'Hour': st.session_state['Hour'],
        'Minute': st.session_state['Minute']
    }
    df = pd.DataFrame([data])
    
    # Predict ETA
    pred = pipeline.predict(df)
    st.session_state['prediction'] = round(pred[0], 2)

    # Save results
    df['prediction'] = st.session_state['prediction']
    df['model_used'] = st.session_state['selected_model']

    history_file_path = 'Data/history.csv'
    df.to_csv(history_file_path, mode='a', header=not os.path.exists(history_file_path), index=False)

if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None

def display_form():
    pipeline = select_model()
    with st.form('input_form'):
        col1, col2 = st.columns(2)
        with col1:
            st.number_input('Origin Latitude', key='Origin_lat')
            st.number_input('Origin Longitude', key='Origin_lon')
            st.number_input('Destination Latitude', key='Destination_lat')
            st.number_input('Destination Longitude', key='Destination_lon')
            st.number_input('Trip Distance (in km)', key='Trip_distance', min_value=0)

        with col2:
            st.number_input('Year', key='Year', min_value=2000, max_value=2100)
            st.number_input('Month', key='Month', min_value=1, max_value=12)
            st.number_input('Day', key='Day', min_value=1, max_value=31)
            st.number_input('Hour', key='Hour', min_value=0, max_value=23)
            st.number_input('Minute', key='Minute', min_value=0, max_value=59)

        st.form_submit_button('Predict ETA', on_click=make_prediction, kwargs=dict(pipeline=pipeline))

if st.session_state['authentication_status']:    
    authenticator.logout(location='sidebar')
    col1, col2 = st.columns(2)
    with col1:
        st.image('resources/eta_image.png', width=200)
    with col2:
        st.header('Predict Estimated Time of Arrival')

    display_form()
    
    final_prediction = st.session_state['prediction']
    if final_prediction is None:
        st.write('### ETA Prediction will be displayed here')
    else:
        st.write(f'### Predicted ETA: {final_prediction} minutes')

else:
    st.info('Please log in to access the app.')
