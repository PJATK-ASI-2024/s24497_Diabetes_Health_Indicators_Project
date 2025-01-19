# Diabetes Health Indicators Project

## 📋 Opis projektu
Celem tego projektu jest stworzenie modelu predykcyjnego, który przewiduje ryzyko wystąpienia cukrzycy u pacjentów na podstawie wskaźników zdrowotnych. Projekt ten analizuje wskaźniki zdrowotne, które mogą mieć wpływ na rozwój cukrzycy, co może wspierać profilaktykę i wczesne wykrywanie choroby oraz pomoc w podejmowaniu decyzji medycznych.

## 📊 Dane
### Diabetes Health Indicators Dataset
- **Źródło danych**: [Kaggle - Diabetes Health Indicators Dataset](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset)
- **Liczba rekordów**: Ponad 250,000 rekordów
- **Atrybuty**:
  - **Zmienna docelowa (`diabetes_binary`)**: 1 – pacjent choruje na cukrzycę, 0 – pacjent nie choruje.
  - **Inne wskaźniki zdrowotne**:
    - `BMI`, `HighBP`, `HighChol`, `CholCheck`, `Smoker`, `Stroke`, `HeartDiseaseorAttack`, `PhysActivity`, `Fruits`, `Veggies`, `HvyAlcoholConsump`, `AnyHealthcare`, `NoDocbcCost`, `GenHlth`, `MentHlth`, `PhysHlth`, `DiffWalk`, `Sex`, `Age`, `Education`, `Income`

## 🎯 Cele projektu
1. **Eksploracja i analiza danych**: Zrozumienie rozkładu wskaźników zdrowotnych i ich związku z ryzykiem cukrzycy.
2. **Trenowanie modelu**: Zbudowanie i optymalizacja modelu predykcyjnego do klasyfikacji ryzyka cukrzycy.
3. **Walidacja i testowanie**: Ewaluacja skuteczności modelu na zbiorze testowym.
4. **Publikacja i wdrożenie**: Przygotowanie modelu do wdrożenia jako API, z możliwością dalszego doszkalania na nowych danych.

## 📂 Struktura projektu
- `src/` - Kod źródłowy projektu
  - `data/` - Skrypty do pobierania i przetwarzania danych
  - `models/` - Definicje modeli
  - `train_model.py` - Skrypt do trenowania modelu
  - `api/` - Kod aplikacji API
    - `app.py` - Główna aplikacja FastAPI
    - `requirements.txt` - Lista zależności
- `airflow_dags/` - Definicje DAGów dla Apache Airflow
- `data/` - Zbiór danych
- `reports/` - Wygenerowane raporty

## 🚀 Uruchomienie projektu

### Wymagania wstępne
- Python 3.10
- [Docker](https://www.docker.com/)
- [Apache Airflow](https://airflow.apache.org/)

### Instalacja
```bash
git clone https://github.com/PJATK-ASI-2024/s24497_Diabetes_Health_Indicators_Project.git
cd s24497_Diabetes_Health_Indicators_Project
pip install -r src/api/requirements.txt
```

### 🔍 Trening modelu
```bash
python src/train_model.py
```
Model zostanie zapisany jako `model.pkl` w katalogu `src/api/`.

### 🖥️ Uruchomienie API
```bash
cd src/api/
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```
Aplikacja będzie dostępna pod adresem `http://localhost:5000`.

### 📌 Testowanie API
```bash
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{
          "bmi": 28.5, 
          "blood_pressure": 120,
          "cholesterol": 200,
          "physactivity": 3,
          "smoker": 0,
          "age": 45,
          "highbp": 1,
          "highchol": 1,
          "cholcheck": 1,
          "stroke": 0,
          "heartdiseaseorattack": 0,
          "hvyalcoholconsump": 0,
          "anyhealthcare": 1,
          "nodocbccost": 0,
          "genhlth": 3,
          "menthlth": 5,
          "physhlth": 7,
          "diffwalk": 0,
          "education": 4,
          "income": 3,
          "fruits": 1,
          "veggies": 1,
          "sex": 1
        }'
```

### 🐳 Uruchomienie z Dockerem
```bash
docker build -t diabetes-api src/api/
docker run -d -p 5000:5000 --name diabetes_api_container diabetes-api
```

### ⚙️ Automatyzacja z Apache Airflow
Projekt wykorzystuje Apache Airflow do automatyzacji procesów ETL oraz trenowania modelu. Wszystkie DAG-i znajdują się w katalogu `airflow_dags/`. Aby uruchomić Airflow:

```bash
export AIRFLOW_HOME=~/airflow
pip install apache-airflow
airflow standalone
```

Następnie w przeglądarce otwórz `http://localhost:8080` i skonfiguruj DAG-i.


