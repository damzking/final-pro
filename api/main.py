import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLoger(__name__)

class EtaFeatures(BaseModel):   
    Origin_lat    :  float            
    Origin_lon    : float                
    Destination_lat    : float           
    Destination_lon  :  float            
    Trip_distance    : int             
    ETA              :  int              
    Year          :  int           
    Day              :  int              
    Month :  int                       
    Hour           : int             
    Minute          :  int 
    

app = FastAPI()

app.add_middleware(
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get('/')
async def RideAPI():
    return {'welcome':'Welcome to my Ride hailing ETA predicting API'}

models = {}
encoder = None
try:
    models = {
        'model1': joblib.load()
        'model2': joblib.load()
        'model3': joblib.load()
        
    }
    
    encoder = joblib.load()
    logger.info('Models and encoder loaded successfully.')
except Exception as e:
    logger.error(f'Error loading models: {e}')
    
    
@app.post('/predict/{model_name}')
async def predict_ETA(model_name: str, data: EtaFeatures):
    try:
        if model_name not in models:
            raise HTTPException(status_code=400, detail='Model not found')
        
        df = pd.DataFrame([data.dict()])
        
        model = models[model_name]
        
        pred = model.predict(df)
        pred = int(pred[0])
        
        decoded_pred = encoder.inverse_transform([pred])[0]
        
        try:
            probability = model.predict_probab(df)[0].tolist()[0]
        except AttributeError:
            probability = 'Probability not available for this model'
        
        return {'model': model_name, 'prediction': decoded_pred, 'probability': probability}
    except HTTPException as e:
        logger.error(f'HTTP Exception: {e.detail}')
        raise e
    except Exception as e:
        logger.error(f'An error occurred durring  prediction: {e}')
        raise HTTPException(status_code=500, detail='Internal Server Error')
    
    if __name__ == '__main__':
        import uvicorn
        uvicorn.run(app, host='0.0.0.0', port=8000)

