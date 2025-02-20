from airflow import DAG
from datetime import datetime,timedelta

from airflow.operators.bash import BashOperator

default_args = {
     'owner': 'goncalo',
     'retries': 5,
     'retry_delay': timedelta(minutes=2)
}

with DAG(
     dag_id="first_dag_example_v0",
     default_args=default_args,
     description="This is a test Goncalo oioioi",
     start_date=datetime(2025,1,1),
     schedule='@daily'
) as dag:
     task1 = BashOperator(
          task_id='first_task',
          bash_command='echo "Hello world!"'
     )
     task1