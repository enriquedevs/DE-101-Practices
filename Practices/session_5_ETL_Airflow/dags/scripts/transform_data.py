import os
import pathlib

import pandas as pd


def main(ti, **kwargs):
    file_name = ti.xcom_pull(task_ids=["step_1_task"])
    AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')

    extracted_data = os.path.join(AIRFLOW_HOME, "dags", "files", "raw", file_name)

    df = pd.read_parquet(extracted_data)

    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    transformed_df: pd.DataFrame = df[['year', 'month', 'day', 'user_id', 'x_coordinate', 'y_coordinate']]
    destination = pathlib.Path(AIRFLOW_HOME, "dags", "files", "clean", file_name)
    transformed_df.to_parquet(destination)

    return [destination]

