import streamlit as st
import joblib
import pandas as pd
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import os

# Set page configuration
st.set_page_config(
    page_title='ETA Prediction',
    page_icon='🕒',
    layout='wide'
)

# Load authentication configuration
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# Cache model loading
@st.cache_resource
def load_GB_model():
    return joblib.load('./models/GB_pipeline.joblib')

@st.cache_resource
def load_XGB_model():
    return joblib.load('./models/XGB_pipeline.joblib')

# Model selection function
def select_model():
    st.selectbox('Select Model', options=['GB_Model', 'XGB_Model'], key='selected_model')
    if st.session_state['selected_model'] == 'GB_Model':
        return load_GB_model()
    else:
        return load_XGB_model()

# Prediction function
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
    prediction = pipeline.predict(df)
    
    st.session_state['prediction'] = prediction

    # Save results
    df['prediction'] = prediction
    df['model_used'] = st.session_state['selected_model']

    history_file_path = 'Data/history.csv'
    df.to_csv(history_file_path, mode='a', header=not os.path.exists(history_file_path), index=False)

    return prediction

if 'prediction' not in st.session_state:
    st.session_state['prediction'] = None

def display_form():
    pipeline = select_model()
    with st.form('input_form'):
        st.markdown('### Trip Details')
        col1, col2 = st.columns(2)
        with col1:
            st.number_input('Origin Latitude', key='Origin_lat', min_value=-0.0, max_value=1000.0)
            st.number_input('Origin Longitude', key='Origin_lon', min_value=-0.0, max_value=1000.0)
            st.number_input('Destination Latitude', key='Destination_lat', min_value=-0.0, max_value=1000.0)
            st.number_input('Destination Longitude', key='Destination_lon', min_value=-0.0, max_value=1000.0)
            st.number_input('Trip Distance (km)', key='Trip_distance')
        with col2:
            st.number_input('Year', key='Year', min_value=2000, max_value=2100)
            st.number_input('Day', key='Day', min_value=1, max_value=31)
            st.number_input('Month', key='Month', min_value=1, max_value=12)
            st.number_input('Hour', key='Hour', min_value=0, max_value=23)
            st.number_input('Minute', key='Minute', min_value=0, max_value=59)
        st.form_submit_button('Predict ETA', on_click=make_prediction, kwargs=dict(pipeline=pipeline))

if st.session_state['authentication_status']:
    authenticator.logout(location='sidebar')
    st.header('🚗 ETA Prediction')
    display_form()
    
    if st.session_state['prediction'] is not None:
        st.write(f'### Predicted ETA: {st.session_state["prediction"]} seconds')
else:
    st.info('Login to gain access to the app')
