#### airflow-test

###### To spin-up the cluster with Airflow
1. `docker compose up airflow-init -d`
2. `docker compose up -d`
3. Access the UI `localhost:8080`

###### To stop Airflow
1. `docker compose down -v` *The `-v` tag is to clear the volumes.*

The folder `/dags/` has some experiments with `py` files used for both local and MWAA.
Airflow reads this folder to use the DAGs inside. If a DAG is not valid, it won't show. If it has an error, it will display on the UI.
