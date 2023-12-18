from airflow import DAG
from datetime import datetime

import forex_common.constants as constants

with DAG(
  "forex",
  start_date=datetime(2023, 2 ,1), 
  schedule_interval="@daily",
  default_args=constants.DEFAULT_ARGS,
  catchup=False
) as dag:
  pass
