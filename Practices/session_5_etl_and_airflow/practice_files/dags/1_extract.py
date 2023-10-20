import os
import pandas

from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime, timedelta

# Default args to not trigger immediately
# You can ignore these for now
default_args = {
  'owner': 'airflow',
  'depends_on_past': False,
  'start_date': datetime(2022, 3, 1),
  'retries': 0,
  'retry_delay': timedelta(minutes=5)
}

# Airflow Folder
AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')

def json2parquet():
  # get the absolute path of input file
  file_input = os.path.join(AIRFLOW_HOME, "dags", "input", "sample.json")
  df = pandas.read_json(file_input)

  # get the path to save a new file
  file_output = os.path.join(AIRFLOW_HOME, "dags", "output",  "sample.parquet")
  # Saving the file as parquet
  df.to_parquet(file_output)

with DAG(
    '1_Extract', # We can find this DAG on airflow Web UI with this name
    default_args=default_args,
    schedule_interval=None,
    concurrency=1,
  ) as dag:
    extract = PythonOperator(
      task_id='Extract',
      python_callable=json2parquet,
      provide_context=True
    )

    # DAG's order (here is only 1, so you can omit and still will work)
    # extract
