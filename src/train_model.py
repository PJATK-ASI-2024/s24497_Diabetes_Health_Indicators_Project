import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score

# Ścieżka do przetworzonego zbioru danych
PROCESSED_DATA_PATH = "data/processed/processed_diabetes_data.csv"
MODEL_PATH = "src/api/model.pkl"

# Sprawdzenie, czy plik istnieje
if not os.path.exists(PROCESSED_DATA_PATH):
    raise FileNotFoundError(f"Plik {PROCESSED_DATA_PATH} nie istnieje. Sprawdź DAG czyszczący dane.")

# Wczytaj dane
df = pd.read_csv(PROCESSED_DATA_PATH, header=0)

# Debugowanie - wypisz dostępne kolumny
print("Dostępne kolumny w DataFrame:", df.columns.tolist())

# Normalizacja nazw kolumn (usuwamy białe znaki i zmieniamy na małe litery)
df.columns = df.columns.str.strip().str.lower()

# Sprawdzenie, czy `diabetes_binary` istnieje
if "diabetes_binary" not in df.columns:
    raise KeyError(" Kolumna 'diabetes_binary' nie została znaleziona. Sprawdź poprawność danych.")

# Podział na cechy i etykiety
X = df.drop(columns=["diabetes_binary"])  # cechy
y = df["diabetes_binary"]  # etykiety

# Podział na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Trenowanie modelu
model = GradientBoostingClassifier(max_depth=6, min_samples_leaf=17, subsample=0.55, learning_rate=0.1)
model.fit(X_train, y_train)

# Ewaluacja
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model wytrenowany! Accuracy: {accuracy:.4f}")

# 📌 Zapis modelu do pliku
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(model, MODEL_PATH)
print(f"Model zapisany jako `{MODEL_PATH}`")
