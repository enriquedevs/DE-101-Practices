import os
import pathlib

import pandas as pd
from uuid import uuid4


def main():
    # Reads JSON data
    AIRFLOW_HOME = os.getenv('AIRFLOW_HOME')
    directory = pathlib.Path(AIRFLOW_HOME, "dags", "files", "input")
    input_files = os.listdir(f"{directory}/")
    destination_files = []
    for input_file in input_files:
        destination_filename = f"{uuid4()}.parquet"
        print(input_file, "mapped to", destination_filename)
        raw_destination = pathlib.Path(AIRFLOW_HOME, "dags", "files", "raw", destination_filename)
        df = pd.read_json(os.path.join(AIRFLOW_HOME, "dags", "files", "input", input_file))
        df.to_parquet(raw_destination)
        destination_files.append(destination_filename)
    return destination_files
