import streamlit as st
import os
import pandas as pd
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Set the page configuration
st.set_page_config(
    page_title='History Page',
    page_icon='🗓',
    layout='wide'
)

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)


def display_historic_predictions():
    st.subheader(":violet[Displaying historic predictions]")
    csv_path = './Dataset/history.csv'
    csv_exists = os.path.isfile(csv_path)

    if csv_exists:
        history = pd.read_csv(csv_path)
        
        st.dataframe(history)
    #return history
        
        
#display_historic_predictions()

        
if st.session_state['authentication_status']:
    authenticator.logout(location='sidebar') 
    #col1, col2 = st.columns(2)
    #with col1:
    #    pass #st.image('resources/imageshist.jfif', width=200)
    #with col2:
    st.header(':rainbow-background[Historic Predictions]') 
    display_historic_predictions()

else:
    st.info('Login to gain access to the app')






