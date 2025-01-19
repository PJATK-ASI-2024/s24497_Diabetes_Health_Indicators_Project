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
    'download_public_split_save',
    default_args=default_args,
    description='Pobieranie danych i podział na zbiory',
    schedule_interval='@daily',
)

RAW_DATA_PATH = "data/raw/diabetes_health_indicators.csv"
PROCESSED_DIR = "data/processed/"

def download_data():
    os.makedirs("data/raw", exist_ok=True)
    url = "https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset/download"
    os.system(f"wget -O {RAW_DATA_PATH} {url}")

def split_data():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    df = pd.read_csv(RAW_DATA_PATH)
    train = df.sample(frac=0.7, random_state=42)
    test = df.drop(train.index)
    train.to_csv(f"{PROCESSED_DIR}/train.csv", index=False)
    test.to_csv(f"{PROCESSED_DIR}/test.csv", index=False)

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

download_task >> split_task
