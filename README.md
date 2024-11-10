# Diabetes Health Indicators Project

## 📋 Opis projektu
Celem tego projektu jest stworzenie modelu predykcyjnego, który przewiduje ryzyko wystąpienia cukrzycy u pacjentów na podstawie wskaźników zdrowotnych. Projekt ten analizuje wskaźniki zdrowotne, które mogą mieć wpływ na rozwój cukrzycy, co może wspierać profilaktykę i wczesne wykrywanie choroby oraz pomoc w podejmowaniu decyzji medycznych.

## 📊 Dane
### Diabetes Health Indicators Dataset
- **Źródło danych**: [Kaggle - Diabetes Health Indicators Dataset](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset)
- **Liczba rekordów**: Ponad 250,000 rekordów
- **Atrybuty**:
  - Zmienna docelowa (`diabetes_binary`): 1 – pacjent choruje na cukrzycę, 0 – pacjent nie choruje.
  - Inne wskaźniki zdrowotne, m.in.:
    - **BMI**: Wskaźnik masy ciała.
    - **Ciśnienie krwi**: Wartość skurczowa i rozkurczowa.
    - **Poziom cholesterolu**: Cholesterol całkowity i HDL.
    - **Aktywność fizyczna**: Poziom aktywności fizycznej.
    - **Palenie papierosów**: Informacja, czy pacjent pali papierosy.
    - **Inne czynniki ryzyka**: Wiek, płeć i inne.

## 🎯 Cele projektu
1. **Eksploracja i analiza danych**: Zrozumienie rozkładu wskaźników zdrowotnych i ich związku z ryzykiem cukrzycy.
2. **Trenowanie modelu**: Zbudowanie i optymalizacja modelu predykcyjnego do klasyfikacji ryzyka cukrzycy.
3. **Walidacja i testowanie**: Ewaluacja skuteczności modelu na zbiorze testowym.
4. **Publikacja i wdrożenie**: Przygotowanie modelu do wdrożenia jako API, z możliwością dalszego doszkalania na nowych danych.

## 📐 Podział danych
- **Trenowanie modelu**: 70% danych (używane do początkowego trenowania modelu).
- **Doszkalanie modelu**: 30% danych (zachowane do dalszego doszkalania).
  
Dane zostaną podzielone za pomocą skryptu `src/split_data.py`, który automatycznie zapisze zbiory w katalogu `data/`.

## 📚 Instrukcja użycia

### 1. Pobranie danych
Pobierz dane z Kaggle i zapisz je w folderze `data/raw/` jako `diabetes_health_indicators.csv`.

### 2. Przygotowanie środowiska
Zainstaluj wymagane biblioteki za pomocą poniższego polecenia:
```bash
pip install -r requirements.txt
```

### 3. Podział danych
Uruchom skrypt `src/split_data.py`, aby podzielić dane na zbiory trenowania i doszkalania:
```bash
python src/split_data.py
```

### 4. Analiza danych i trenowanie modelu
Przeprowadź analizę i trenuj model, otwierając notebooki w katalogu `notebooks/`:
- `exploratory_data_analysis.ipynb`: Analiza eksploracyjna wskaźników zdrowotnych.
- `model_training.ipynb`: Notebook z trenowaniem i oceną modelu predykcyjnego.

## 📋 Wymagania systemowe
- Python 3.x
- Pakiety: `pandas`, `scikit-learn`, `matplotlib`, `seaborn`, `numpy`
