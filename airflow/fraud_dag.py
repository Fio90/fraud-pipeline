from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'frederick',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2026, 1, 1),
}

# Define the DAG
with DAG(
    dag_id='fraud_pipeline',
    default_args=default_args,
    description='End to end fraud detection pipeline',
    schedule='@daily',
    catchup=False,
    tags=['fraud', 'pipeline']
) as dag:

    # Task 1 - Data ingestion
    load_data = BashOperator(
        task_id='load_data',
        bash_command='cd /opt/fraud-pipeline && python ingestion/load_data.py',
    )

    # Task 2 - dbt transformation
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /opt/fraud-pipeline/dbt_project/fraud_pipeline && dbt run',
    )

    # Task 3 - ML scoring
    train_model = BashOperator(
        task_id='train_model',
        bash_command='cd /opt/fraud-pipeline && python ml/train_model.py',
    )

    # Define task order
    load_data >> dbt_run >> train_model