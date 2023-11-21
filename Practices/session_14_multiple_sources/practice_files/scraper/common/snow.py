import pandas
from snowflake.connector import connect, SnowflakeConnection

from common.constants import SNOW_CREDS, TABLE_NAME

conn = connect(
  user=SNOW_CREDS['user'],
  password=SNOW_CREDS['password'],
  account=SNOW_CREDS['account'],
  warehouse=SNOW_CREDS['warehouse'],
  database=SNOW_CREDS['database'],
  schema=SNOW_CREDS['schema']
)

def upload_to_snowflake(connection: SnowflakeConnection, data_frame: pandas.DataFrame):
  with connection.cursor() as cursor:
    column_secrets = ['%s'] * len(data_frame.columns)
    column_preparated_str = ','.join(column_secrets)
    query = f"INSERT INTO {TABLE_NAME} VALUES ({column_preparated_str})"
    cursor.executemany(query, data_frame.values.tolist())

def handle_csv(data: list, company:str, year:str, month:str, state:str):
  columns = data[0]
  data_values = data[1:]
  df = pandas.DataFrame(data_values, columns=columns)
  df = add_extra_cols(df, company, year, month, state)
  upload_to_snowflake(conn, df)

def handle_json(data: list, company:str, year:str, month:str, state:str):
  df = pandas.DataFrame.from_dict(data)
  df = add_extra_cols(df, company, year, month, state)
  upload_to_snowflake(conn, df)

def add_extra_cols(df: pandas.DataFrame, company:str, year:str, month:str, state:str):
  df['company'] = company
  df['year'] = year
  df['month'] = month
  df['state'] = state
  return df