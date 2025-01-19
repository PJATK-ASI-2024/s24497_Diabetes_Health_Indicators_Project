from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'building_model',
    default_args=default_args,
    description='Trenowanie modelu ML',
    schedule_interval='@daily',
)

PROCESSED_DATA_PATH = "data/processed/processed_diabetes_data.csv"
MODEL_PATH = "src/api/model.pkl"

def train_model():
    df = pd.read_csv(PROCESSED_DATA_PATH)

    X = df.drop(columns=["diabetes_binary"])
    y = df["diabetes_binary"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = GradientBoostingClassifier(max_depth=6, min_samples_leaf=17, subsample=0.55, learning_rate=0.1)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    joblib.dump(model, MODEL_PATH)
    print(f"Model zapisany! Accuracy: {accuracy:.4f}")

train_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag,
)
