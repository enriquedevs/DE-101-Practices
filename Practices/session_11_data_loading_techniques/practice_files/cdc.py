import pandas
import os
from snowflake.connector import connect, SnowflakeConnection

def upload_to_snowflake(connection: SnowflakeConnection, data_frame, table_name):
  with connection.cursor() as cursor:
    query = f"INSERT INTO {table_name} (name, description, price, stock, valid_for_year) VALUES (%s, %s, %s, %s, %s)"
    data = data_frame[['name', 'description', 'price', 'stock', 'valid_for_year']].values.tolist()

    cursor.executemany(query, data)

with connect(
    account="<SNOWFLAKE_LOCATOR>",
    user="<SNOWFLAKE_USERNAME>",
    password="<SNOWFLAKE_PASSWORD>",
    database="<SNOWFLAKE_DB>",
    schema="<SNOWFLAKE_DB_SCHEMA>",
    warehouse="<SNOWFLAKE_WAREHOUSE>",
    region="<SNOWFLAKE_AWS_REGION>"
) as connection:
  list_dir = os.listdir("practice_files")

  for file_name in list_dir:
    df = pandas.read_csv(f'./practice_files/{file_name}')

    _, year = file_name.split("_")
    year = year.replace(".csv", "")
    df["valid_for_year"] = year

    upload_to_snowflake(connection, df, "products")
