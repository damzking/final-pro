import streamlit as st
import pandas as pd
#import plotly.express as px
#import plotly.graph_objects as go
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title='Data Page',
    page_icon='🗃',
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

@st.cache_data
def load_data0():
    data0 = pd.read_csv('Dataset/Train.csv')
    return data0 

@st.cache_data
def load_data():
    data1 = pd.read_csv('Dataset/merged.csv')
    return data1


# Function to get all columns from a specific table
st.cache_resource()
def get_all_column():
    data0 = pd.read_csv('Dataset/Train.csv')
    data1 = pd.read_csv('Dataset/merged.csv')
    st.session_state['data0'], st.session_state['data1'] = data0, data1

# Initialize the dataframe in session state if not already there
if 'data0' not in st.session_state and 'data1' not in st.session_state:
    get_all_column()
    


            
