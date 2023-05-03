import json
import os
import pathlib

import pandas as pd


def main(**kwargs):
    file_name = kwargs.pop("file_name")
    AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')

    directory = pathlib.Path(AIRFLOW_HOME, "dags", "files", "clean", file_name)
    df = pd.read_parquet(directory)
    df.to_parquet(pathlib.Path(AIRFLOW_HOME, "dags", "files", "output"))
