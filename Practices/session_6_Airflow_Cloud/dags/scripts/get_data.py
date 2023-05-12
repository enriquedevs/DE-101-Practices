import io
import os
import uuid
from datetime import datetime

import pandas as pd
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


def read_s3(hook, s3_bucket_name, input_file):
    data = hook.read_key(
        bucket_name=s3_bucket_name,
        key=input_file
    )
    return data


def write_to_s3(hook, df, s3_bucket_name, execution_time_str):
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    hook.load_file_obj(
        buffer,
        key=os.path.join("raw", execution_time_str, f"{uuid.uuid4()}.parquet"),
        bucket_name=s3_bucket_name,
        replace=True
    )


def main(s3_bucket_name, aws_conn_id):
    execution_time = datetime.now()
    execution_time_str = execution_time.strftime("%d-%m-%Y %H:%M")
    # Reads JSON data
    hook = S3Hook(aws_conn_id=aws_conn_id)
    input_files = hook.list_keys(
        bucket_name=s3_bucket_name,
        prefix='input/'
    )
    for input_file in input_files:
        if not input_file.endswith(".json"):
            continue
        json_data = read_s3(hook, s3_bucket_name, input_file)
        df = pd.read_json(json_data, orient="records")
        write_to_s3(hook, df, s3_bucket_name, execution_time_str)

    return [execution_time_str]
