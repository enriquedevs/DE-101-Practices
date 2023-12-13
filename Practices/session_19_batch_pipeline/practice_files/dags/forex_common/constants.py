import os
from datetime import timedelta

DEFAULT_ARGS = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "admin@localhost.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

CONN_ID_HIVE = 'forex_hive_conn'
CONN_ID_SLACK = 'forex_slack_conn'

CONN_ID_SPARK = 'forex_spark_conn'
PYSPARK_SCRIPT = os.getenv('AIRFLOW_HOME') + '/dags/forex_scripts/upload_hive.py'
