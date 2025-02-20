from airflow import DAG
# from airflow.operators.docker_operator import DockerOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import json

# Define default arguments
default_args = {
    'owner': 'goncalo',
    'start_date': datetime(2024, 2, 1),
    'retries': 4
}

# Define the DAG
dag = DAG(
    'converted_argo_workflow',
    default_args=default_args,
    schedule_interval=None
)

# Task 1: list-py-set
list_py_set = DockerOperator(
    task_id='list_py_set',
    image="ghcr.io/qcdis/naavre-cells-openlab/list-py-set-gabriel-pelouze-lifewatch-eu:latest",
    api_version='auto',
    auto_remove="success",
    command="source /venv/bin/activate; python /app/task.py --id 1ca0d5e",
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    # volumes=["/tmp/data"],
    dag=dag
)

# Task 2: splitter (Python function)
def splitter(**kwargs):
    ti = kwargs['ti']
    names_json = ti.xcom_pull(task_ids='list_py_set')
    names_list = json.loads(names_json)
    list_of_lists = [[name] for name in names_list]
    ti.xcom_push(key='splitter_output', value=json.dumps(list_of_lists))

splitter_task = PythonOperator(
    task_id='splitter',
    python_callable=splitter,
    provide_context=True,
    dag=dag
)

# Task 3: list-py-process
list_py_process = DockerOperator(
    task_id='list_py_process',
    image="ghcr.io/qcdis/naavre-cells-openlab/list-py-process-gabriel-pelouze-lifewatch-eu:latest",
    api_version='auto',
    auto_remove="success",
    command="source /venv/bin/activate; python /app/task.py --names '{{ ti.xcom_pull(task_ids='splitter', key='splitter_output') }}' --param_greeting_template 'Hello, {}!' --id 9eb8967",
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    # volumes=["/tmp/data"],
    dag=dag
)

# Define dependencies
list_py_set >> splitter_task >> list_py_process
