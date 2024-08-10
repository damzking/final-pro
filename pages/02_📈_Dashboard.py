import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

import plotly.graph_objects as go



st.set_page_config(
    page_title='Dashboard Page',
    page_icon='📊',
    layout='wide'
)

# Load configuration for authentication
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# Caching the data loading function
@st.cache_data()

def load_train_data():
    Train_df = pd.read_csv('./Dataset/Train.csv')
    return Train_df

Train_df = load_train_data()

def final_indicator():
    st.markdown(f"""
        <div style= "background-color: turquoise; border-radius: 10px; width: 60%; margin-top: 20px;" >
            <h3 style="margin-left: 30px">Quick Stats About Dataset</h3>
            <hr>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    # Add your final indicator widgets here (e.g., using st.metric, st.caption, etc.)
    st.write('---')

def eda_dashboard():
    st.subheader('Exploratory Data Analysis')
    col1, col2, col3 = st.columns(3)
    
    # Convert DataFrame by dropping unnecessary columns
    train_df_noid = Train_df.drop(['ID', 'Timestamp', 'Month_name', 'Day_name'], axis=1, errors='ignore')

    # Plot Boxplots
    with col1:
        for variable in train_df_noid.columns:
            fig = px.box(train_df_noid, y=variable, title=f'Boxplot of {variable}', color_discrete_sequence=['lightcoral'])
            st.plotly_chart(fig, use_container_width=True)

    # Plot Histograms
    with col2:
        for variable in train_df_noid.columns:
            fig = px.histogram(train_df_noid, x=variable, title=f'Histogram of {variable}', color_discrete_sequence=['skyblue'])
            st.plotly_chart(fig, use_container_width=True)

    # Plot KDE with Violin Plots
    with col3:
        for variable in train_df_noid.columns:
            fig = px.histogram(train_df_noid, x=variable, title=f'KDE of {variable}', marginal="violin", color_discrete_sequence=['lightcoral'])
            st.plotly_chart(fig, use_container_width=True)

    # Additional plots (if needed)
    col1, col2 = st.columns(2)
    with col1:
        fignum = px.histogram(train_df_noid.select_dtypes(include=np.number), barmode='overlay', title='Distribution of Numerical Variables')
        st.plotly_chart(fignum)
        
    with col2:
        figcat = px.box(train_df_noid.select_dtypes(include=np.number), title='Boxplot of Numerical Variables')
        st.plotly_chart(figcat)
    
    col1, col2 = st.columns(2)
    with col1:
        fignum = px.histogram(train_df_noid.select_dtypes(include=np.number), barmode='overlay', title='Distribution of Tenure, Monthly Charges & Total Charges')
        st.plotly_chart(fignum)
        
    with col2:
        figcat = px.box(train_df_noid.select_dtypes(include=np.number), title='Boxplot of Numerical Variables')
        st.plotly_chart(figcat)
    
    

   
        
#@st.cache_data()
def kpi_dashboard():    
    final_indicator()
    
    
    

            
if st.session_state['authentication_status']:
    authenticator.logout(location='sidebar')
    col1, col2 = st.columns(2)
    with col1:
        pass

    with col2:
        st.title(':rainbow-background[EDA & Dashboard]')
        st.selectbox('Select Dashboard', options=['EDA', 'KPI'], key='selected_dashboard')
    if st.session_state['selected_dashboard'] == 'EDA':
        eda_dashboard()
    elif st.session_state['selected_dashboard'] == 'KPI':
        kpi_dashboard()

else:
    st.info('Login to gain access to the app')
