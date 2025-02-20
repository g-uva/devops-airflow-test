from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

with DAG(
    dag_id='test_docker_import',  # Different ID to avoid conflicts
    start_date=datetime(2023, 10, 27),
    schedule=None,
    catchup=False
) as dag:
    test_docker = DockerOperator(
        task_id='test_docker',
        image='hello-world',  # Simple test image
    )