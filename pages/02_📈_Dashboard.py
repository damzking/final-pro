import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

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

@st.cache_data()
def load_train_weath_data():
    train_weath_df = pd.read_csv('./Dataset/merged.csv')
    return train_weath_df

# Corrected function calls
Train_df = load_train_data()
train_weath_df = load_train_weath_data()

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

def kpi_dashboard():
    st.write("### Weather Data Analysis")
    
    col4, col5, col6 = st.columns(3)

    with col4:
        st.write("#### 1. What is the Average ETA by Day of the Week?")
        # Plot Average ETA by Day of the Week
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        train_weath_df['Day_name'] = pd.Categorical(train_weath_df['Day_name'], categories=day_order, ordered=True)
        average_eta_per_day = train_weath_df.groupby('Day_name')['ETA'].mean().sort_index().reset_index()

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(average_eta_per_day['Day_name'], average_eta_per_day['ETA'], color='lightcoral')
        ax.set_title('Average ETA by Day of the Week')
        ax.set_xlabel('Day of the Week')
        ax.set_ylabel('Average ETA')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col5:
        st.write("#### 2. What is the Average Speed by Different Weather Conditions?")
        # Plot Average Speed by Weather Condition
        train_weath_df['Average_Speed'] = train_weath_df['Trip_distance'] / train_weath_df['ETA']
        weather_conditions = [
            'dewpoint_2m_temperature', 
            'maximum_2m_air_temperature',  
            'minimum_2m_air_temperature', 
            'surface_pressure', 
            'total_precipitation', 
            'u_component_of_wind_10m', 
            'v_component_of_wind_10m'
        ]

        fig, axes = plt.subplots(3, 3, figsize=(15, 10))
        axes = axes.flatten()
        for idx, condition in enumerate(weather_conditions):
            avg_speed = train_weath_df.groupby(condition)['Average_Speed'].mean().reset_index()
            axes[idx].bar(avg_speed[condition], avg_speed['Average_Speed'], color='skyblue')
            axes[idx].set_title(f'Average Speed by {condition}')
            axes[idx].set_xlabel(condition)
            axes[idx].set_ylabel('Average Speed (m/s)')
            axes[idx].grid(axis='y')
            plt.xticks(rotation=45)

        plt.tight_layout()
        st.pyplot(fig)

    with col6:
        st.write("#### 3. What is the Average Trip Distance by Month?")
        # Plot Average Trip Distance by Month
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.violinplot(x="Month_name", y="Trip_distance", data=train_weath_df, color='lightcoral', ax=ax)
        ax.set_title('Average Trip Distance by Month')
        plt.xticks(rotation=45)
        st.pyplot(fig)

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
