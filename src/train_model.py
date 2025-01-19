import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score

#Wczytaj dane
df = pd.read_csv("data/processed/processed_diabetes_data.csv")

#Podział na cechy i etykiety
X = df.drop(columns=["diabetes_binary"])  # cechy
y = df["diabetes_binary"]  # etykiety

#Podział na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Trenowanie modelu
model = GradientBoostingClassifier(max_depth=6, min_samples_leaf=17, subsample=0.55, learning_rate=0.1)
model.fit(X_train, y_train)

#Ewaluacja
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")

#Zapis modelu do pliku
joblib.dump(model, "src/api/model.pkl")
print("Model zapisany jako `model.pkl`")
