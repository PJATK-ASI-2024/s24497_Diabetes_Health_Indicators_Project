from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel

app = FastAPI()

# Wczytaj model
model = joblib.load("model.pkl")

class Features(BaseModel):
    bmi: float
    blood_pressure: float
    cholesterol: float
    physical_activity: float
    smoking: int
    age: int


@app.post("/predict")
def predict(features: Features):
    data = np.array([[features.bmi, features.blood_pressure, features.cholesterol,
                      features.physical_activity, features.smoking, features.age]])
    prediction = model.predict(data)
    return {"diabetes_risk": int(prediction[0])}

@app.get("/")
def health_check():
    return {"status": "API is running"}
