from airflow import DAG
from airflow.utils.task_group import TaskGroup
from datetime import datetime
from airflow.providers.http.sensors.http import HttpSensor
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.utils.task_group import TaskGroup

import forex_common.constants as constants
import forex_common.api as f_api
import forex_common.path as f_path
import forex_scripts.download_rates as download_rates
from forex_common.utils import slack_message

with DAG(
  "forex",
  start_date=datetime(2023, 2 ,1), 
  schedule_interval="@daily",
  default_args=constants.DEFAULT_ARGS,
  catchup=False
) as dag:
  with TaskGroup("health_check", tooltip="Initial Check") as health_check:
    is_forex_rates_available = HttpSensor(
      task_id="is_forex_rates_available",
      http_conn_id=f_api.CONN_ID,
      endpoint=f_api.BASE_PATH,
      response_check=lambda response: "rates" in response.text,
      poke_interval=5,
      timeout=20
    )

    is_forex_currencies_file_available = FileSensor(
      task_id="is_forex_currencies_file_available",
      fs_conn_id=f_path.CONN_ID,
      filepath=f_path.CSV,
      poke_interval=5,
      timeout=20
    )

    is_forex_rates_available
    is_forex_currencies_file_available

    

  download_rates = PythonOperator(
    task_id="download_rates",
    python_callable=download_rates.save2local
  )
  save2hdfs = BashOperator(
    task_id="save2hdfs",
    bash_command="""
      hdfs dfs -put -f $AIRFLOW_HOME/dags/data/forex_rates.json /forex
    """
  )

  forex_processing = SparkSubmitOperator(
    task_id="forex_processing",
    application=constants.PYSPARK_SCRIPT,
    conn_id=constants.CONN_ID_SPARK,
    verbose=False
  )
  send_slack_notification = SlackWebhookOperator(
    task_id="slack_notification",
    http_conn_id=constants.CONN_ID_SLACK,
    message=slack_message('Enrique')
  )
  remove_temp = BashOperator(
      task_id='remove_temp_files',
      bash_command="""
        rm $AIRFLOW_HOME/dags/data/forex_rates.json
      """
  )

  health_check >> download_rates >> save2hdfs
  save2hdfs >> [remove_temp, forex_processing]
  forex_processing >> send_slack_notification
