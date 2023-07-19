from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime, timedelta
import json

# Define the DAG parameters
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'max_active_runs': 1
}


# Define the function to read the JSON file from S3, convert it to CSV, and write it back to S3
def json_to_csv(s3_bucket_name, s3_key_name, aws_conn_id):
    # Instantiate the S3Hook with your AWS credentials
    print("Connecting to S3")
    hook = S3Hook(aws_conn_id=aws_conn_id)
    print("Airflow S3Hook connected to S3")

    # Read the JSON file from S3
    input_json = hook.read_key(s3_key_name, s3_bucket_name)
    print(input_json)

    # Convert the JSON data to CSV format
    data = json.loads(input_json)
    csv_string = 'user_id, x_coordinate, y_coordinate, date\n'
    for row in data:
        csv_string += f'{row["user_id"]}, {row["x_coordinate"]}, {row["y_coordinate"]}, {row["date"]}\n'
    print(csv_string)

    print("Writing CSV to S3")
    # Write the CSV data back to S3
    hook.load_string(
        csv_string,
        key="output.csv",
        bucket_name=s3_bucket_name,
        replace=True
    )
    print("CSV was written to S3")


# Define the DAG
with DAG('aws_dag', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:
    # Define the task that calls the json_to_csv function
    json_to_csv_task = PythonOperator(
        task_id='json_to_csv',
        python_callable=json_to_csv,
        op_kwargs={
            's3_bucket_name': 's3-enroute-public-bucket',
            's3_key_name': 'input.json',
            'aws_conn_id': 'aws_conn'
        }
    )


# Set the task dependencies
# noinspection PyStatementEffect
json_to_csv_task
