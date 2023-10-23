from airflow import DAG
from datetime import datetime, timedelta

default_args = {
  'owner': 'airflow',
  'depends_on_past': False,
  'start_date': datetime(2022, 3, 1),
  'retries': 0,
  'retry_delay': timedelta(minutes=5)
}

with DAG('etl_s3', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:
    pass
