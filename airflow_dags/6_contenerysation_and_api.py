from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 20),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'containerization_and_api',
    default_args=default_args,
    description='Budowa obrazu Dockera i publikacja na Docker Hub',
    schedule_interval='@daily',
)

docker_build = BashOperator(
    task_id='build_docker',
    bash_command='docker build -t my-docker-image src/api/',
    dag=dag,
)

docker_push = BashOperator(
    task_id='push_docker',
    bash_command='docker push my-docker-image',
    dag=dag,
)

docker_build >> docker_push
