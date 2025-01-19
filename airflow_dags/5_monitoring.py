from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import joblib
import numpy as np
import requests
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'monitoring',
    default_args=default_args,
    description='Analiza dokładności modelu i powiadomienia',
    schedule_interval='@daily',
)

MODEL_PATH = "src/api/model.pkl"

def test_model():
    model = joblib.load(MODEL_PATH)
    sample_input = np.array([[28.5, 120, 200, 3, 0, 45]])
    prediction = model.predict(sample_input)
    print(f"Przewidywana klasa: {prediction[0]}")

def send_alert():
    requests.post("https://api.sendgrid.com/v3/mail/send",
        headers={"Authorization": "Bearer" + os.environ["SENDGRID_API_KEY"],},
        json={
            "personalizations": [{"to": [{"email": "pawelpllukasiewicz@gmail.com"}]}],
            "from": {"email": "s24497@pjwstk.edu.pl"},
            "subject": "❗ Uwaga: Problem z modelem ML",
            "content": [{"type": "text/plain", "value": "Model wykazuje niski poziom dokładności!"}]
        })

test_task = PythonOperator(
    task_id='test_model',
    python_callable=test_model,
    dag=dag,
)

alert_task = PythonOperator(
    task_id='send_alert',
    python_callable=send_alert,
    dag=dag,
)

test_task >> alert_task
