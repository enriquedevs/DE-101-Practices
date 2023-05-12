import pandas as pd
import json
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 3, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('xcom_dag', default_args=default_args, schedule_interval=None)


def extract_data():
    # Reads JSON data
    print("Extracting JSON File Data")

    with open('/opt/airflow/dags/735d1fb5-fbfb-4dd6-bbca-b4da4a9a6a97.json') as f:
        json_data = json.load(f)

    return json.dumps(json_data)


def transform_data(extracted_data):
    # Transform the extracted_data by using dataframes
    print("Starting Transformations")

    df = pd.DataFrame(json.loads(extracted_data))
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    transformed_df = df[['year', 'month', 'day', 'user_id', 'x_coordinate', 'y_coordinate']]

    print("Transformations made!")
    return transformed_df.to_csv(index=False)


def load_data(transformed_data):
    # Write transformed data to CSV file
    print("Writing transformed data into CSV file")
    with open("/opt/airflow/dags/output.csv", "w") as csv:
        csv.write(transformed_data)
    print("Data Loaded into CSV File")


t1 = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag
)

t2 = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    op_kwargs={'extracted_data': "{{ task_instance.xcom_pull(task_ids='extract_data', key='return_value') }}"},
    dag=dag
)

t3 = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    op_kwargs={'transformed_data': "{{ task_instance.xcom_pull(task_ids='transform_data', key='return_value') }}"},
    dag=dag
)

# noinspection PyStatementEffect
t1 >> t2 >> t3
