from datetime import datetime, timedelta

from airflow import DAG, XComArg
from airflow.operators.python import PythonOperator

from scripts import get_data, transform_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 3, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG('aws_s3_dag',
         default_args=default_args,
         schedule_interval=None,
         concurrency=3,
         ) as dag:
    step_1 = PythonOperator(
        task_id='step_1_task',
        python_callable=get_data.main,
        op_kwargs=dict(
            s3_bucket_name='s3-enroute-public-bucket',
            aws_conn_id='aws_conn'
        )
    )

    step_2 = PythonOperator(
        task_id='step_2_task',
        python_callable=transform_data.main,
        op_kwargs=dict(
            execution_time_inp=XComArg(step_1),
            s3_bucket_name='s3-enroute-public-bucket',
            aws_conn_id='aws_conn'
        )
    )

    # noinspection PyStatementEffect
    step_1 >> step_2
