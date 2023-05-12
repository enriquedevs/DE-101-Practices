import io
import os
from io import BytesIO

import pandas as pd
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


def read_s3(hook, s3_bucket_name, input_file):

    # this returns a s3 Object
    obj = hook.get_key(
        bucket_name=s3_bucket_name,
        key=input_file
    )
    return io.BytesIO(obj.get()["Body"].read())


def write_to_s3(hook, df, s3_bucket_name, file_name):
    buffer = io.BytesIO()
    df.to_parquet(buffer, index=False)
    buffer.seek(0)
    hook.load_file_obj(
        buffer,
        key=os.path.join("clean", file_name),
        bucket_name=s3_bucket_name,
        replace=True
    )


def main(execution_time_inp: str, s3_bucket_name, aws_conn_id):
    hook = S3Hook(aws_conn_id=aws_conn_id)
    execution_time = execution_time_inp[0]
    raw_files = hook.list_keys(
        bucket_name=s3_bucket_name,
        prefix=f'raw/{execution_time}/'
    )
    for file_name in raw_files:
        if not file_name.endswith(".parquet"):
            continue

        data = read_s3(hook, s3_bucket_name, file_name)
        df = pd.read_parquet(data)

        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        transformed_df: pd.DataFrame = df[['year', 'month', 'day', 'user_id', 'x_coordinate', 'y_coordinate']]

        write_to_s3(hook, transformed_df, s3_bucket_name, file_name.replace("raw/", ""))
