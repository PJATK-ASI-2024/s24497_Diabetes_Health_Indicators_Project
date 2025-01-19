import joblib
import numpy as np

# Wczytaj model
model = joblib.load("src/api/model.pkl")

# Przykładowe dane testowe (fikcyjne wartości wskaźników zdrowotnych)
sample_input = np.array([[28.5, 120, 200, 3, 0, 45]])  # (BMI, Blood Pressure, Cholesterol, Physical Activity, Smoking, Age)

# Przewidywanie
prediction = model.predict(sample_input)
print(f"Przewidywana klasa: {prediction[0]}")  # 0 - brak cukrzycy, 1 - ryzyko cukrzycy
