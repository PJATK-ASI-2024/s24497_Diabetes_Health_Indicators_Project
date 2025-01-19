import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
import logging

app = FastAPI()

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Wczytanie modelu
try:
    model = joblib.load("model.pkl")
    logger.info(f"Model załadowany poprawnie! Oczekuje {model.n_features_in_} cech.")
except Exception as e:
    logger.error(f"Błąd ładowania modelu: {e}")
    model = None

# Endpoint główny (health check)
@app.get("/")
def read_root():
    return {"message": "API działa poprawnie"}

# Endpoint predykcji
@app.post("/predict")
def predict(data: dict):
    try:
        logger.info(f"Otrzymane dane: {data}")

        # Pobranie wymaganych nazw cech z modelu
        expected_features = model.feature_names_in_
        logger.info(f"Oczekiwane cechy: {expected_features}")

        # Sprawdzenie, czy wszystkie cechy są w JSON-ie
        missing_features = [feature for feature in expected_features if feature not in data]
        if missing_features:
            raise ValueError(f"Brakuje cech: {missing_features}")

        # Tworzenie tablicy cech w poprawnej kolejności
        feature_values = [data[feature] for feature in expected_features]
        features = np.array([feature_values])

        # Sprawdzenie poprawności liczby cech
        if features.shape[1] != model.n_features_in_:
            raise ValueError(f"Niepoprawna liczba cech! Oczekiwano {model.n_features_in_}, ale otrzymano {features.shape[1]}.")

        prediction = model.predict(features)
        logger.info(f"Przewidywana wartość: {prediction[0]}")

        return {"prediction": int(prediction[0])}

    except KeyError as e:
        logger.error(f"Brakująca wartość w JSON: {e}")
        raise HTTPException(status_code=400, detail=f"Brak klucza: {e}")

    except Exception as e:
        logger.error(f"Błąd serwera: {e}")
        raise HTTPException(status_code=500, detail=str(e))
