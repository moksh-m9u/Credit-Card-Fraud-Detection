from fastapi import FastAPI, HTTPException, Body
from typing import List
from schema.user_input import user_input
from fastapi.responses import JSONResponse
import pickle
import pandas as pd 
from pathlib import Path
import os

MODEL_VERSION = "1.0.0"
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "fraud_model.pkl"

app=FastAPI(
    title="Credit CardFraud Detection API",
    description=(
        "A production-ready REST API for detecting fraudulent credit card transactions. "
    ),
    version="1.0.0",
    contact={
        "name": "Moksh",
        "email": "moksh1326@gmail.com",
    }
)


with open(MODEL_PATH,'rb')as f:
    model=pickle.load(f)

@app.get('/')
def home():
    return {'message': 'Welcome to the Credit Card Fraud Detection API'}

@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
    }

@app.post('/predict')
def predict(userdata: user_input = Body(
    ...,
    openapi_examples={
        "example_fraud": {
            "summary": "A fraudulent transaction",
            "value": {
                "V14": -4.289254, "V10": -2.772272, "V12": -2.899907, "V4": 3.997906,
                "V17": -2.830056, "V3": -1.609851, "V11": 3.202033, "V16": -1.140747, "Amount": 0.00
            }
        },
        "example_normal": {
            "summary": "A normal transaction",
            "value": {
                "V14": -0.311169, "V10": 0.090794, "V12": -0.617800, "V4": 1.378155,
                "V17": 0.207971, "V3": 2.536346, "V11": -0.551599, "V16": -0.470400, "Amount": 149.62
            }
        }
    }
)):
    try:
        input_df = pd.DataFrame([userdata.model_dump(exclude_none=True)])

        proba = float(model["model"].predict_proba(input_df)[0][1])
        threshold = model["threshold"]
        prediction = int(proba >= threshold)

        return JSONResponse(status_code=200, content={
            "prediction": prediction,
            "label": "fraud" if prediction == 1 else "legit",
            "confidence": round(proba, 4),
            "threshold_used": threshold
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail='internal server error')

@app.post('/predict/batch')
def predict_batch(users: List[user_input] = Body(
    ...,
    openapi_examples={
        "example_batch_mixed": {
            "summary": "A mixed batch of fraud and normal transactions",
            "value": [
                {
                    "V14": -4.289254, "V10": -2.772272, "V12": -2.899907, "V4": 3.997906,
                    "V17": -2.830056, "V3": -1.609851, "V11": 3.202033, "V16": -1.140747, "Amount": 0.00
                },
                {
                    "V14": -0.311169, "V10": 0.090794, "V12": -0.617800, "V4": 1.378155,
                    "V17": 0.207971, "V3": 2.536346, "V11": -0.551599, "V16": -0.470400, "Amount": 149.62
                },
                {
                    "V14": -1.470102, "V10": -1.525412, "V12": -6.560124, "V4": 2.330243,
                    "V17": -4.781831, "V3": -0.359745, "V11": 2.032912, "V16": -2.282194, "Amount": 239.93
                },
                {
                    "V14": -0.143772, "V10": -0.166974, "V12": 1.065235, "V4": 0.448154,
                    "V17": -0.114804, "V3": 0.166480, "V11": 1.612727, "V16": 0.463917, "Amount": 2.69
                },
                {
                    "V14": -6.771097, "V10": -4.801637, "V12": -10.912819, "V4": 2.679787,
                    "V17": -12.598419, "V3": -2.592844, "V11": 4.895844, "V16": -7.358083, "Amount": 59.00
                }
            ]
        },
        "example_batch_normal": {
            "summary": "A batch of only normal transactions",
            "value": [
                {
                    "V14": -0.165946, "V10": 0.207643, "V12": 0.066084, "V4": 0.379780,
                    "V17": 1.109969, "V3": 1.773209, "V11": 0.624501, "V16": -2.890083, "Amount": 378.66
                },
                {
                    "V14": -0.287924, "V10": -0.054952, "V12": 0.178228, "V4": -0.863291,
                    "V17": -0.684093, "V3": 1.792993, "V11": -0.226487, "V16": -1.059647, "Amount": 123.50
                },
                {
                    "V14": -1.119670, "V10": 0.753074, "V12": 0.538196, "V4": 0.403034,
                    "V17": -0.237033, "V3": 1.548718, "V11": -0.822843, "V16": -0.451449, "Amount": 69.99
                }
            ]
        },
        "example_batch_fraud": {
            "summary": "A batch of only fraudulent transactions",
            "value": [
                {
                    "V14": -4.289254, "V10": -2.772272, "V12": -2.899907, "V4": 3.997906,
                    "V17": -2.830056, "V3": -1.609851, "V11": 3.202033, "V16": -1.140747, "Amount": 0.00
                },
                {
                    "V14": -1.692029, "V10": -0.838587, "V12": -0.503141, "V4": 2.288644,
                    "V17": 0.599717, "V3": 1.088463, "V11": -0.414575, "V16": 0.666780, "Amount": 529.00
                },
                {
                    "V14": -6.079337, "V10": -2.447469, "V12": -4.609628, "V4": 4.732795,
                    "V17": 6.739384, "V3": -4.304597, "V11": 2.101344, "V16": 2.581851, "Amount": 1.00
                }
            ]
        }
    }
)):
    try:
        # Extract validated dictionary from each user in the list
        input_data = [u.model_dump(exclude_none=True) for u in users]
        
        # Create a single DataFrame (much faster than looping over model.predict)
        input_df = pd.DataFrame(input_data)
        
        # Predict all transactions at once
        probas = model["model"].predict_proba(input_df)[:, 1]
        threshold = model["threshold"]
        
        results = []
        for proba in probas:
            prediction = int(proba >= threshold)
            results.append({
                "prediction": prediction,
                "label": "fraud" if prediction == 1 else "legit",
                "confidence": round(float(proba), 4)
            })

        return JSONResponse(status_code=200, content={
            "results": results,
            "threshold_used": threshold
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail='internal server error')