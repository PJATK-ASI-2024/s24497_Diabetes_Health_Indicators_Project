import os
import pandas as pd
from sklearn.model_selection import train_test_split

# Ścieżki do plików
RAW_DATA_PATH = "data/raw/diabetes_health_indicators.csv"
PROCESSED_DATA_PATH = "data/processed/processed_diabetes_data.csv"
TRAIN_FEATURES_PATH = "data/processed/train_features.csv"
TRAIN_LABELS_PATH = "data/processed/train_labels.csv"
TEST_FEATURES_PATH = "data/processed/test_features.csv"
TEST_LABELS_PATH = "data/processed/test_labels.csv"

# Sprawdzenie, czy foldery istnieją, jeśli nie, tworzymy je
os.makedirs("data/processed", exist_ok=True)

def clean_and_split_data():
    # Wczytaj dane
    print("Wczytywanie danych...")
    data = pd.read_csv(RAW_DATA_PATH)

    # Informacje o danych
    print("Podstawowe informacje o danych:")
    print(data.info())

    # Oczyszczanie danych
    print("Oczyszczanie danych...")
    data_cleaned = data.dropna()

    # Zapisz przetworzone dane
    data_cleaned.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Przetworzone dane zapisane w: {PROCESSED_DATA_PATH}")

    # Podział danych na cechy i etykiety
    X = data_cleaned.drop(columns=["Diabetes_binary"])
    y = data_cleaned["Diabetes_binary"]

    # Podział na zbiory treningowe i testowe
    print("Podział danych na zbiory treningowe i testowe...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Zapisanie podzielonych danych
    X_train.to_csv(TRAIN_FEATURES_PATH, index=False)
    y_train.to_csv(TRAIN_LABELS_PATH, index=False)
    X_test.to_csv(TEST_FEATURES_PATH, index=False)
    y_test.to_csv(TEST_LABELS_PATH, index=False)

    print("Zbiory danych zostały zapisane:")
    print(f"- Zbiór treningowy: {TRAIN_FEATURES_PATH}, {TRAIN_LABELS_PATH}")
    print(f"- Zbiór testowy: {TEST_FEATURES_PATH}, {TEST_LABELS_PATH}")

if __name__ == "__main__":
    clean_and_split_data()