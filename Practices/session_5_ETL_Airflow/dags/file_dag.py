from datetime import datetime, timedelta

from airflow import DAG, XComArg
from airflow.operators.python import PythonOperator

from scripts import get_data, transform_data, load_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 3, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('file_dag',
         default_args=default_args,
         schedule_interval=None,
         concurrency=3,
         ) as dag:
    step_1 = PythonOperator(
        task_id='step_1_task',
        python_callable=get_data.main,
        provide_context=True
    )

    step_2 = PythonOperator(
        task_id='step_2_task',
        python_callable=transform_data.main,
        provide_context=True,
    )

    step_3 = PythonOperator(
        task_id='step_3_task',
        python_callable=load_data.main,
        provide_context=True,
    )

    # noinspection PyStatementEffect
    step_1 >> step_2 >> step_3
