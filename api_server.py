from fastapi import FastAPI, Request
import json
import pickle
import pandas as pd
from pandas import json_normalize
import ipaddress
from sklearn.base import BaseEstimator, TransformerMixin
from transformer import IpToNumericTransformer, DurationTransformer

app = FastAPI()

# Load the trained anomaly detection model
with open('pipeline.pkl', 'rb') as f:
    pipeline = pickle.load(f)

@app.post("/logs")
async def receive_logs(request: Request):
    
    log_data = await request.json()
    
    # Flatten the nested fields like 'netflow' into columns
    df = json_normalize(log_data)
    
    # Use the anomaly detection model to predict anomalies
    prediction = pipeline.predict(df)

    # Add predictions back to the DataFrame
    df['prediction'] = prediction

    json_data = df.to_dict(orient='records')
    
    if prediction == 1 :
        
        for record in json_data:
            record['@timestamp'] = pd.to_datetime(record['@timestamp'])
            record['netflow.first_switched'] = pd.to_datetime(record['netflow.first_switched'])
            record['netflow.last_switched'] = pd.to_datetime(record['netflow.last_switched'])
            record['@timestamp'] = record['@timestamp'].isoformat()
            record['netflow.first_switched'] = record['netflow.first_switched'].isoformat()
            record['netflow.last_switched'] = record['netflow.last_switched'].isoformat()
            
        return {"status": "Anomaly detected"}
    else:
        return {"status": "Normal traffic"}
