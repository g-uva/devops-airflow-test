from airflow import DAG
from airflow.operators.python import PythonOperator # For demo
from datetime import datetime
from your_fission_operator import FissionOperator # Import your custom operator

with DAG(
    dag_id='fission_workflow',
    start_date=datetime(2023, 10, 26),
    schedule_interval=None,
    catchup=False
) as dag:

    run_container_task = FissionOperator(
        task_id='run_container',
        fission_function_name='my-container-function', # Unique name
        container_image='your-docker-image:latest',
        command=['/app/my-script.sh'],  # Optional command
        environment_name='my-fission-env' # Optional environment
    )

    # Example of a regular Python task (for orchestration)
    def _do_something():
        print("Airflow task running alongside Fission tasks")

    do_something = PythonOperator(
        task_id='do_something',
        python_callable=_do_something
    )

    run_container_task >> do_something # Example dependency