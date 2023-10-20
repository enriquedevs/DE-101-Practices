import os
import pandas

from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta

default_args = {
  'owner': 'airflow',
  'depends_on_past': False,
  'start_date': datetime(2022, 3, 1),
  'retries': 0,
  'retry_delay': timedelta(minutes=5)
}

AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')

def json2parquet():
  file_input = os.path.join(AIRFLOW_HOME, "dags", "input", "sample.json")
  df = pandas.read_json(file_input)

  file_output = os.path.join(AIRFLOW_HOME, "dags", "output",  "sample.parquet")
  df.to_parquet(file_output)

  return file_output

def parquet_columns(parquet_file):
  file_input = parquet_file
  df = pandas.read_parquet(file_input, engine='pyarrow') # Add engine to decode

  # Transform
  df['date'] = pandas.to_datetime(df['date'], format='%Y-%m-%d')
  df['year'] = df['date'].dt.year
  df['month'] = df['date'].dt.month
  df['day'] = df['date'].dt.day
  transformed_df = df[['year', 'month', 'day', 'user_id', 'x_coordinate', 'y_coordinate']]

  # get the path to save a new file
  file_output = os.path.join(AIRFLOW_HOME, "dags", "output",  "sample_columns.parquet")
  # Saving the file as parquet
  transformed_df.to_parquet(file_output)
  return file_output

with DAG(
    '2_Transform',
    default_args=default_args,
    schedule_interval=None,
    concurrency=1,
  ) as dag:
    extract = PythonOperator(
      task_id='Extract',
      python_callable=json2parquet,
      provide_context=True
    )
    transform = PythonOperator(
      task_id='Transform',
      python_callable=parquet_columns,
      op_kwargs={'parquet_file': "{{ task_instance.xcom_pull(task_ids='Extract', key='return_value') }}"},
      provide_context=True
    )

    extract >> transform
