import streamlit as st
import joblib
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier

from xgboost import XGBClassifier
import os
import datetime
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title='Predict Page',
    page_icon='🔍',
    layout='wide'
)


with open('.streamlit/config.yaml') as file:
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


st.cache_resource(show_spinner= 'Model Loading....')
def select_model():
    col1, col2 = st.columns(2)
    
    with col1:
        st.selectbox('Select Model', options=['GB_Model', 'XGB_Model'], key='selected_model')

    with col2:
        pass
    
    if st.session_state['selected_model'] == 'XGB_Model':
        pipeline = load_XGB_model()

    else:
        pipeline = load_GB_model()
    
    return pipeline

def make_predictions(pipeline, df):
    pred = pipeline.predict(df)
    prediction = int(pred[0])
    return prediction

def main():
    st.title("ETA Prediction Application")

    # Initialize session state for prediction and probability
    if 'predictions' not in st.session_state:
        st.session_state['predictions'] = None

    # Select model 
    pipeline = select_model()

    # Display and download results
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

    # Make predictions
        if st.button("Make Predictions"):
            prediction = make_predictions(pipeline, df)
            if prediction is not None :
                st.session_state["prediction"] = prediction
                df['Predictions'] = prediction if prediction is not None else 'N/A'

                
                df['model_used'] = st.session_state['selected_model']

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Predictions",
                data=csv,
                file_name='predictions.csv',
                mime='text/csv',
            )
    else:
        st.warning("Please upload a CSV file.")

if st.session_state['authentication_status']:    
    authenticator.logout(location='sidebar')
    col1, col2 = st.columns(2)
    with col1:
        st.image('Resources/image.jpg', width=600)
    with col2:
        st.header(':rainbow-background[Estimated time of arrival Prediction]')

    main()


else:
    st.info('Login to gain access to the app')