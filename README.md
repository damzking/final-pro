# ETA-PREDICTION-FOR-DELIVERY-COMPANY
![estimated-time-of-arrival](https://github.com/user-attachments/assets/4f3a989b-7b55-4c96-ad68-f5258a964bed)

## Project Overview 📖

In this project, we utilize supervised machine learning techniques, Ride-hailing apps, such as Uber and Yassir, depend heavily on real-time data and machine learning algorithms to optimize their services. Predicting the estimated time of arrival (ETA) accurately for Yassir trips is crucial for enhancing service reliability and customer satisfaction. An accurate ETA prediction not only improves user experience but also boosts business efficiency by enabling better resource allocation. This hackathon aims to develop a solution to predict the ETA at the dropoff point for a single Yassir journey, thereby directly contributing to the company's operational success and customer trust.
Developed a machine learning model to accurately predict the estimated time of arrival for individual journeys on a ride-hailing platform..

## Project Summary 📄

| Project Name | Deployed App | Streamlit website application |
|--------------|--------------|------------------------------|
| Yassir ETA prediction |[Docker Hub](https://hub.docker.com/repositories/victoranim)|[webapp](https://ride-hailing-eta-prediction.onrender.com)|

The project is guided by the CRISP-DM (Cross-Industry Standard Process for Data Mining) framework.

## Project Structure 📂

- `Dataset/`: Contains the dataset used for analysis, and predicted values.
- `Notebook/`: Contains jupyter notebook with full end-to-end ML process
- `models/`: Pipeline with ML model
- `.gitignore`: Holds files to be ignored by Git.
- `api`: Contains the backend Working app for prediction
- `Frontend`: Contains the backend Working app for prediction
- `pages`: Contains our streamlit website app for prediction
- `LICENSE`: Project license.
- `README.md`: Project overview, links, highlights, and information.
- `requirements.txt`: Required libraries & packages

## Getting Started🏁

You need to have [`Python 3`](https://www.python.org/) on your system. Then you can clone this repo and being at the repo's `root :: repository_name> ...`

1. Clone this repository: `git clone https://github.com/Koanim/ETA-PREDICTION-FOR-DELIVERY-COMPANY.git`
2. On your IDE, create A Virtual Environment and Install the required packages for the project:

- Windows:
        
        python -m venv venv; 
        venv\Scripts\activate; 
        python -m pip install -q --upgrade pip; 
        python -m pip install -qr requirements.txt  

- Linux & MacOs:
        
        python3 -m venv venv; 
        source venv/bin/activate; 
        python -m pip install -q --upgrade pip; 
        python -m pip install -qr requirements.txt  

The two lengthy command lines share the same structure, utilizing the ` ; ` symbol to pipe multiple commands. However, you can execute each command manually, one after the other.

- **Create the Python's virtual environment** that isolates the required libraries of the project to avoid conflicts;
- **Activate the Python's virtual environment** so that the Python kernel & libraries will be those of the isolated environment;
- **Upgrade Pip, the installed libraries/packages manager** to have the up-to-date version that will work correctly;
- **Install the required libraries/packages** listed in the `requirements.txt` file so that they can be imported into the python script and notebook without any issue.

**NB:** For MacOs users, please install `Xcode` if you have an issue.

## Run FastAPI

- Run the API (being at the repository root):
        
  FastAPI:
    
    - Main

          cd api, uvicorn main:app --reload 

    <!-- - ETA prediction

          cd api, uvicorn mainp:app --reload  -->


  - Go to your browser at the local port, to explore the API's documentation :
        
      http://127.0.0.1:8000/docs


## Run Streamlit App
        
  Streamlit:
  
          streamlit run 1_💒_Home.py 

## Docker App Screenshots

- App documentation


- Input


- Prediction


## Author✍️

Victor Nyarko Anim

Visit me on [LinkedIn](https://www.linkedin.com/in/victor-anim-83115818/) and [Medium](https://medium.com/@victor.nyarko)



---

Feel free to star ⭐ this repository if you find it helpful!


## Acknowledgments 🙏

I would like to express my gratitude to the [Azubi Africa Data Analyst Program](https://www.azubiafrica.org/data-analytics) for their support and for offering valuable projects as part of this program. Not forgeting my scrum masters on this project [Rachel Appiah-Kubi](https://www.linkedin.com/in/racheal-appiah-kubi/) & [Emmanuel Koupoh](https://github.com/eaedk)

## License 📜

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Contact 📧

For questions, feedback, and collaborations, please contact [Aminu Oluwarotimi Desmond](aminuoluwarotimi@gmail.com).











