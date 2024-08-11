import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Set up the page configuration
st.set_page_config(
    page_title='Home Page',
    page_icon='',
    layout='wide'
)


def background():
    st.header("Welcome to :rainbow[Estimated Time of Arrival Prediction App]")
    col1, col2 = st.columns(2)

    with col1:
        st.image('Resources/image.jpg', width=500)
    with col2:
        st.caption("""
            For more information about me, checkout my
            :red[[GitHub](https://github.com/Koanim/ETA-PREDICTION-FOR-DELIVERY-COMPANY), [LinkedIn](https://www.linkedin.com/in/aminudesmond/)]""")

        st.caption("##### Contact Me 📧")
        st.caption(""" 
            - Need help with this app?
            - Interested in collaborating on a project?
            - Have feedback or inquiries?
        """)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            with st.container():
                st.write('#### About App')
                st.caption(
                    "This app predicts the estimated time of arrival (ETA) for deliveries using two different machine learning model pipelines: XGBoost and Gradient Boosting.")
                st.caption("\nIt provides accurate and real-time ETA predictions for both new and existing deliveries, helping streamline operations and improve customer satisfaction.")
                st.caption("\nThe history feature of this app stores all predictions made, allowing for later analysis to evaluate the accuracy of each model. This data can be used to determine which models perform best, providing insights for future improvements.")
                st.write("#### Key Features of App")

            with st.expander(":violet[**Data Page**] -"):
                st.caption('This page displays the datasets used to train our machine learning models, including statistical information. The datasets were sourced from the Azubi Africa platform and cleaned before modeling.')

            with st.expander(":violet[**Dashboard Page**] -"):
                st.caption('The dashboard consists of two types of visualizations:')
                st.caption('1. **EDA (Exploratory Data Analysis)**: Visualizations that help understand the characteristics and distribution of the dataset variables.')
                st.caption('2. **KPI**: These visualizations focus on key performance indicators, especially in relation to the target variable, :red[Estimated time of arrival]. They help us understand how other variables impact :red[Estimated time of arrival].')

            with st.expander(":violet[**Predict Page**] -"):
                st.caption('The predict page allows users to input responses for variables such as :orange[Origin_latitude, Origin_longitude, Destination_latitude, Destination_longitude, Trip_distance, Year, Day, Month, Hour, Minute]. You can then select which model to use for your prediction.')

            with st.expander(':violet[**History Page**] -'):
                st.caption('This page records all predictions made by the app. The stored data can help determine if the models need improvement and identify which model is the most accurate.')

            with st.expander(':violet[**Bulk Predict Page**] -'):
                st.caption('Upload data with columns and data types similar to the original dataset. After clicking the predict button, you will receive prediction values for each row.')

        with col2:
            st.write('#### :rainbow[Estimated Time of Arrival Overview]')
            st.write("""
                Estimated Time of Arrival (ETA) is a critical component in ride-hailing apps like Uber and Yassir, playing a vital role in ensuring a seamless and efficient user experience. ETA refers to the predicted time it takes for a driver to arrive at a passenger's pickup location.
            """)
            st.markdown("""
                Accurate ETA predictions are crucial for several reasons:
                - **Customer Satisfaction:** Accurate ETA estimates provide customers with reliable information about when their ride will arrive. This improves their overall experience and satisfaction. Reliable ETAs build trust with customers, leading to higher retention rates and positive reviews.
                - **Operational Efficiency:** By predicting ETAs more accurately, Yassir can optimize the distribution of drivers and resources. This ensures that drivers are effectively assigned to rides based on demand and proximity, reducing idle time and improving operational efficiency. Improved ETA predictions can help reduce operational costs by minimizing wait times and inefficient routes. This leads to better fuel usage and lower overall costs.
                - **Competitive Advantage:** In a competitive market, offering more accurate ETAs can differentiate Yassir from its competitors. This can attract more users and partners who value reliability and efficiency. Accurate ETAs can enhance relationships with business partners by providing them with reliable scheduling information and improving the overall service experience.
                - **Impact on Business Strategy:** Savings from improved efficiency can be reinvested into other areas of the business, such as technology upgrades, marketing, or expansion efforts. Leveraging real-time data and advanced analytics can drive strategic decisions and foster innovation within the company.
            """)

            col1, col2 = st.columns(2)
            with col1:
                with st.container():
                    with st.expander("###### :rainbow[ANALYTICAL QUESTIONS]"):
                        st.write("""
                            The following analytical questions will help us gain insight and confirm our hypothesis:
                            - Which day of the week has the most significant impact on ETA, and how does the average ETA vary across different days?
                            - What is the highest average speed of travel under each weather condition (dewpoint_2m_temperature, maximum_2m_air_temperature, minimum_2m_air_temperature, surface_pressure, total_precipitation, u_component_of_wind_10m, v_component_of_wind_10m)?
                            - Which month has the highest average trip distance?
                            - Is there a relationship between trip distance and ETA?
                            - What are the most common (top 10) origins and destinations in terms of latitude and longitude?
                        """)

            with col2:
                with st.expander("###### :rainbow[HYPOTHETICAL QUESTIONS]"):
                    st.write("""
                        The following hypothesis will be tested:
                        - Surface pressure above the average does not have a significantly more positive impact on reducing the Estimated Time of Arrival (ETA) compared to surface pressure below the average.
                    """)

# Load authentication configuration
with open('.streamlit/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

name, authentication_status, username = authenticator.login(location='sidebar')

# User login and authentication logic
if authentication_status:
    st.sidebar.write(f'Welcome {username}')
    authenticator.logout(location='sidebar')

    if st.sidebar.button('Reset Password'):
        st.session_state['reset_password'] = True

    if st.session_state.get('reset_password'):
        with st.form('reset_password_form'):
            new_password = st.text_input('Enter new password', type='password')
            confirm_password = st.text_input('Confirm new password', type='password')
            if st.form_submit_button('Reset'):
                if new_password == confirm_password:
                    try:
                        authenticator.reset_password(username, new_password, location='sidebar')
                        st.session_state['reset_password'] = False
                        st.success('Password modified successfully')
                    except Exception as e:
                        st.error(e)
                else:
                    st.error('Passwords does not match 😕')

    background()

elif authentication_status is False:
    st.info('Invalid Email/Password 😕')

elif authentication_status is None:
    st.info('Please use the test account below to access the app')

    if st.sidebar.button('Create Password'):
        st.session_state['Create Password'] = True

    if st.session_state.get('Create Password'):
        with st.form('Create account'):
            name = st.text_input('Enter your name')
            username = st.text_input('Enter your username')
            email = st.text_input('Enter your email')
            password = st.text_input('Enter your password', type='password')
            confirm_password = st.text_input('Confirm password', type='password')
            if st.form_submit_button('Register'):
                if password == confirm_password:
                    try:
                        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(name, username, email, password, pre_authorization=False, location='sidebar')
                        if email_of_registered_user:
                            st.success('User registered successfully')
                            st.balloons()
                            st.session_state['Create Password'] = False
                    except Exception as e:
                        st.error(e)
                else:
                    st.error('😕 Passwords does not match')

    st.code("""
        Test Account
        Username: guser
        Password: guestuser
    """)
