from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'download_cloud_clean_standard_normalize_save',
    default_args=default_args,
    description='Pobieranie danych modelowych, czyszczenie, normalizacja i zapis',
    schedule_interval='@daily',
)

PROCESSED_DIR = "data/processed/"

def clean_and_normalize():
    df = pd.read_csv(f"{PROCESSED_DIR}/train.csv")

    # Czyszczenie danych – usuwanie braków
    df.dropna(inplace=True)

    # Normalizacja cech numerycznych
    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[num_cols] = (df[num_cols] - df[num_cols].mean()) / df[num_cols].std()

    # Zapis do pliku
    df.to_csv(f"{PROCESSED_DIR}/processed_diabetes_data.csv", index=False)

clean_task = PythonOperator(
    task_id='clean_and_normalize',
    python_callable=clean_and_normalize,
    dag=dag,
)
