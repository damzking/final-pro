import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Updated EtaFeatures without the ETA field
class EtaFeatures(BaseModel):
    Origin_lat: float
    Origin_lon: float
    Destination_lat: float
    Destination_lon: float
    Trip_distance: int
    Year: int
    Day: int
    Month: int
    Hour: int
    Minute: int

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def RideAPI():
    return {'welcome': 'Welcome to my Ride hailing ETA predicting API'}

models = {}
try:
    models = {
        'GB_Model': joblib.load('../models/GB_pipeline.joblib'),
        'XGB_Model': joblib.load('../models/XGB_pipeline.joblib'),
    }
    logger.info('Models loaded successfully.')
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

        return {'model': model_name, 'prediction': int(pred[0])}
    
    except HTTPException as e:
        logger.error(f'HTTP Exception: {e.detail}')
        raise e
    except Exception as e:
        logger.error(f'An error occurred during prediction: {e}')
        raise HTTPException(status_code=500, detail='Internal Server Error')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
