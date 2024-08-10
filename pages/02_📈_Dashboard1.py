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

st.set_page_config(
    page_title = 'Dashboard Page',
    page_icon = '📊',
    layout = 'wide'
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


@st.cache_data()
def load_concat_data():
    concat_df = pd.read_csv('Data/df_churn.csv')
    return concat_df

concat_df = load_concat_data()

def final_indicator():
            st.markdown(f"""
                <div style= "background-color: turquoise; border-radius: 10px; width: 60%; margin-top: 20px;" >
                    <h3 style="margin-left: 30px">Quick Stats About Dataset</h3>
                    <hr>
                </div>
                """,
                unsafe_allow_html=True
                )
            
            col1,col2,col3 = st.columns(3)
            with col1:
                st.caption(f"###### Churn Rate: :orange[**{(concat_df['Churn'].value_counts(normalize = True).get('Yes', 0)* 100):.2f}%**]")
                st.caption(f"###### Average Tenure (Months) : :orange[**{concat_df['tenure'].mean():.2f}**]")

            with col2:
                    st.caption(f"###### Count of Churned Customers : :orange[**{concat_df['Churn'].value_counts().get('Yes')}**]")
                    st.caption(f"###### Count of Retained Customers : :orange[**{concat_df['Churn'].value_counts().get('No')}**]")

            with col3:
                    st.caption(f"###### Average Total Charges: :orange[**${concat_df['TotalCharges'].mean():.2f}**]")
                    st.caption(f"###### Average Monthly Charges: :orange[**${concat_df['MonthlyCharges'].mean():.2f}**]")
            st.write('---')      

#@st.cache_data()
def eda_dashboard():
    
    st.subheader(' Exploratory Data Analysis')
    col1, col2, col3 = st.columns(3)

    with col1:
        fig = px.histogram(concat_df, x='tenure', nbins=100, title='Distribution of Tenure', color_discrete_sequence=['springgreen', 'lemonchiffon'])
        st.plotly_chart(fig)
    
        catp1 = px.box(concat_df, x= 'tenure', title='Boxplot of Tenure', color_discrete_sequence=['springgreen', 'lemonchiffon'])
        st.plotly_chart(catp1)

    with col2:    
        fig1 = px.histogram(concat_df, x='MonthlyCharges', nbins=100, title='Distribution of Monthly Charges', color_discrete_sequence=['royalblue', 'lemonchiffon'])
        st.plotly_chart(fig1)

        figc1 = px.box(concat_df, x='MonthlyCharges', title='Boxplot of Monthly Charges', color_discrete_sequence=['royalblue', 'lemonchiffon'])
        st.plotly_chart(figc1)   
    
    with col3:
    
        fig2 = px.histogram(concat_df, x='TotalCharges', nbins=100, title='Distribution of Total Charges', color_discrete_sequence=['magenta', 'lemonchiffon'])
        st.plotly_chart(fig2)
    
        catp1 = px.box(concat_df, x= 'TotalCharges', title='Boxplot of Total Charges', color_discrete_sequence=['magenta', 'lemonchiffon'])
        st.plotly_chart(catp1) 
    
    col1, col2 = st.columns(2)
    with col1:
        fignum = px.histogram(concat_df.select_dtypes(include=np.number), barmode='overlay', title='Distribution of Tenure, Monthly Charges & Total Charges')
        st.plotly_chart(fignum)
        
    with col2:
        figcat = px.box(concat_df.select_dtypes(include=np.number), title='Boxplot of Numerical Variables')
        st.plotly_chart(figcat)
    
    sns.set(style="ticks")
    pairplot = sns.pairplot(concat_df, hue='Churn', height=1.5, aspect=2)
    plt.subplots_adjust(top=0.9)
    plt.suptitle('Customer Churn Pairplot', fontsize=20)

    for ax in pairplot.axes.flatten():
        for label in ax.get_xticklabels():
            label.set_rotation(45)
        for label in ax.get_yticklabels():
            label.set_rotation(45)
    st.pyplot(pairplot)
        
#@st.cache_data()
def kpi_dashboard():    
    final_indicator()
    
    
    st.subheader('KPI Analysis')
    col1, col2, col3 = st.columns(3)
    with col1:
        fig4 = px.histogram(concat_df, x='Churn', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Number of Churned Customers')
        st.plotly_chart(fig4)
    
    with col2:    
        fig5 = px.histogram(concat_df, x='Contract', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Type of Contract and Customer Churn')
        st.plotly_chart(fig5)

    with col3:    
        fig6 = px.histogram(concat_df, x='PaymentMethod', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Type of Payment Method and Customer Churn')
        st.plotly_chart(fig6)
        
    col4, col5, col6 =st.columns(3)
    with col4:
        fig7 = px.histogram(concat_df, x='gender', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Gender and Customer Churn')
        st.plotly_chart(fig7)
    with col5:
        fig8 = px.histogram(concat_df, x='SeniorCitizen', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Senior Citizen and Customer Churn')
        st.plotly_chart(fig8)
    with col6:
        fig9 = px.histogram(concat_df, x='Partner', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Customers with Partner and Churn')
        st.plotly_chart(fig9)
        
    col1, col2, col3 = st.columns(3)
    with col1:
        fig10 = px.histogram(concat_df, x='InternetService', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Internet Service and Customer Churn')
        st.plotly_chart(fig10)
    with col2:
        fig11 = px.histogram(concat_df, x='OnlineSecurity', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Online Security and Customer Churn')
        st.plotly_chart(fig11)
    with col3:
        fig12 = px.histogram(concat_df, x='OnlineBackup', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Online Backup and Customer Churn')
        st.plotly_chart(fig12)
        
    col1, col2, col3 = st.columns(3)
    with col1:
        fig13 = px.histogram(concat_df, x='DeviceProtection', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Device Protection and Customer Churn')
        st.plotly_chart(fig13)
    with col2:
        fig14 = px.histogram(concat_df, x='TechSupport', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Tech Support and Customer Churn')
        st.plotly_chart(fig14)
    with col3:
        fig15 = px.histogram(concat_df, x='StreamingTV', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Streaming TV and Customer Churn')
        st.plotly_chart(fig15)
        
    col1, col2 = st.columns(2)
    with col1:
        fig16 = px.histogram(concat_df, x='StreamingMovies', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Streaming Movies and Churned Customers')
        st.plotly_chart(fig16)
    with col2:
        fig17 = px.histogram(concat_df, x='PaperlessBilling', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Paperless Billing and Churned Customers')
        st.plotly_chart(fig17)
        
    col1, col2, col3 = st.columns(3)
    with col1:
        fig19 = px.histogram(concat_df, x='tenure', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Tenure and Churned Customers')
        st.plotly_chart(fig19)
    with col2:
        fig20 = px.histogram(concat_df, x='MonthlyCharges', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Monthly Charges and Churned Customers')
        st.plotly_chart(fig20)
    with col3:
        fig21 = px.histogram(concat_df, x='TotalCharges', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Total Charges and Churned Customers')
        st.plotly_chart(fig21)
    
    col7, col8, col9 =st.columns(3)
    with col7:    
        catplot1 = px.box(concat_df, x='gender', y= 'tenure', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='How long it took Customers to Churn')
        st.plotly_chart(catplot1)

    with col8:
        catplot2 = px.box(concat_df, x='Contract', y= 'tenure', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Which Contract type did Customers Churned')
        st.plotly_chart(catplot2)
        
    with col9:
        cat1 = px.bar(concat_df, x='SeniorCitizen', y= 'tenure', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Did Senior Citizens Churn')
        st.plotly_chart(cat1)
        
    col1, col2, col3 = st.columns(3)
    with col1:
        kpi1 = px.bar(concat_df, x='Dependents', y= 'tenure', color='Churn', color_discrete_map={'Yes':'turquoise', 'No':'slateblue'}, title='Customers with Dependents and Churn')
        st.plotly_chart(kpi1)
    
    with col2 and col3:
        kp2 = sns.catplot(data=concat_df, x='gender', y='tenure', hue='Churn', kind='bar', col='PaymentMethod', aspect=.7, palette=['blue', 'red'])
        st.pyplot(kp2)


            
if st.session_state['authentication_status']:
    authenticator.logout(location='sidebar')
    col1, col2 = st.columns(2)
    with col1:
        st.image('resources/dashb1.jpg', width=200)
        st.title('Dashboard')
        if st.checkbox('Show data'):
            st.subheader('Telco churn data')
            st.write(concat_df)

    with col2:
        st.title(':rainbow-background[EDA & Dashboard]')
        st.selectbox('Select Dashboard', options=['EDA', 'KPI'], key='selected_dashboard')
    if st.session_state['selected_dashboard'] == 'EDA':
        eda_dashboard()
    elif st.session_state['selected_dashboard'] == 'KPI':
        kpi_dashboard()

else:
    st.info('Login to gain access to the app')
