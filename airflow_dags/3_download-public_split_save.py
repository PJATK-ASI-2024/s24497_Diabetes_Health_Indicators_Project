from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import os
import gspread
from google.oauth2.service_account import Credentials

# Konfiguracja Google Sheets
GOOGLE_SHEETS_CREDENTIALS = "config/credentials.json"  # Plik z kluczami
SPREADSHEET_NAME = "DiabetesHealthIndicators"  # Nazwa Twojego arkusza

# Domyślne argumenty DAG-a
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'download_public_split_save',
    default_args=default_args,
    description='Pobieranie danych, podział i zapis do Google Sheets',
    schedule_interval='@daily',
)

RAW_DATA_PATH = "data/raw/diabetes_health_indicators.csv"
PROCESSED_DIR = "data/processed/"


# Pobranie danych
def download_data():
    os.makedirs("data/raw", exist_ok=True)
    url = "https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset/download"
    os.system(f"wget -O {RAW_DATA_PATH} {url}")


# Podział danych
def split_data():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df = pd.read_csv(RAW_DATA_PATH)
    train = df.sample(frac=0.7, random_state=42)
    test = df.drop(train.index)

    train.to_csv(f"{PROCESSED_DIR}/train.csv", index=False)
    test.to_csv(f"{PROCESSED_DIR}/test.csv", index=False)


# Zapis do Google Sheets
def save_to_google_sheets():
    creds = Credentials.from_service_account_file(GOOGLE_SHEETS_CREDENTIALS,
                                                  scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)

    # Otwórz arkusz
    spreadsheet = client.open(SPREADSHEET_NAME)

    # Przetwarzanie danych i zapis do Google Sheets
    for dataset, sheet_name in [("train.csv", "Modelowy"), ("test.csv", "Douczeniowy")]:
        df = pd.read_csv(f"{PROCESSED_DIR}/{dataset}")
        worksheet = spreadsheet.worksheet(sheet_name)

        # Czyszczenie arkusza i zapis danych
        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())


download_task = PythonOperator(
    task_id='download_data',
    python_callable=download_data,
    dag=dag,
)

split_task = PythonOperator(
    task_id='split_data',
    python_callable=split_data,
    dag=dag,
)

save_task = PythonOperator(
    task_id='save_to_google_sheets',
    python_callable=save_to_google_sheets,
    dag=dag,
)

download_task >> split_task >> save_task
