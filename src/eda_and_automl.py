import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sweetviz as sv
from tpot import TPOTClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import json

# Wczytanie danych przetworzonych
print("Wczytywanie danych...")
data = pd.read_csv("data/processed/processed_diabetes_data.csv")

# Podstawowa eksploracja danych
print("Podstawowe informacje o danych:")
print(data.info())
print("\nStatystyki opisowe:")
print(data.describe())

# Analiza brakujących danych
missing_values = data.isnull().sum()
print("\nBrakujące wartości w danych:")
print(missing_values[missing_values > 0])

# Histogramy zmiennych numerycznych
print("Generowanie histogramów...")
data.hist(figsize=(12, 10))
plt.tight_layout()
plt.savefig("reports/histograms.png")
plt.show()

# Wykresy pudełkowe dla wybranych zmiennych
print("Generowanie wykresów pudełkowych...")
plt.figure(figsize=(10, 6))
sns.boxplot(data=data[["BMI", "MentHlth", "PhysHlth"]])
plt.title("Boxplots for Selected Variables")
plt.savefig("reports/boxplots.png")
plt.show()

# Macierz korelacji
print("Generowanie macierzy korelacji...")
correlation_matrix = data.corr()
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.savefig("reports/correlation_matrix.png")
plt.show()

# Automatyczny raport Sweetviz
print("Generowanie raportu Sweetviz...")
report = sv.analyze(data)
report.show_html(filepath="reports/sweetviz_report.html", open_browser=False)

# Przygotowanie danych do AutoML
print("Podział danych na cechy i etykiety...")
X = data.drop(columns=["Diabetes_binary"])
y = data["Diabetes_binary"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# AutoML za pomocą TPOT
print("Uruchamianie AutoML za pomocą TPOT...")
tpot = TPOTClassifier(generations=5, population_size=50, verbosity=2, random_state=42, cv=5)
tpot.fit(X_train, y_train)

# Wyświetlanie najlepszego modelu
print("Najlepszy model znaleziony przez TPOT:")
print(tpot.fitted_pipeline_)

# Ewaluacja modelu
y_pred = tpot.predict(X_test)
classification_rep = classification_report(y_test, y_pred, output_dict=True)
accuracy = accuracy_score(y_test, y_pred)

# Wyświetlanie wyników ewaluacji
print("\nRaport klasyfikacji:")
print(classification_report(y_test, y_pred))
print("Dokładność modelu:", accuracy)

# Zapis wyników ewaluacji do JSON
metrics = {
    "accuracy": accuracy,
    "classification_report": classification_rep
}

with open("reports/metrics.json", "w") as metrics_file:
    json.dump(metrics, metrics_file, indent=4)
print("Metryki zapisane do pliku: reports/metrics.json")

# Zapisanie najlepszego modelu
tpot.export("reports/best_model.py")
print("Najlepszy model zapisany do: reports/best_model.py")
