import os
import shutil
import numpy
import pandas
from sqlalchemy import create_engine

from common.constants import PATH, SQL_FILE_TABLE_NAME, CREATE_TABLE, SQL_FILE, Format

FOLDER_SEPARATOR = '/'
FILE_SEPARATOR = '_'

rng = numpy.random.default_rng()
# Returns a random between 0 and 1.999...
def decimal_random():
  ret = rng.integers(low=0,high=2) + rng.random()
  return ret

def create_root_dir(format: Format):
  path = PATH['base_folder']
  create_dir(path)

  path = f"{path}/{format.value}"
  try:
    os.mkdir(path)
  except:
    shutil.rmtree(path)
    os.mkdir(path)

def create_sql_file():
  path = PATH['base_folder']
  path = f'{path}/sql'

  try:
    os.remove(path)
  except:
    pass

  with open(f'{path}/{SQL_FILE}', 'w') as file:
    file.write(CREATE_TABLE + '\n\n')

def create_dir(path: str):
  try:
    os.mkdir(path)
  except:
    pass

def get_format(format: str):
  if (format == Format.CSV.value):
    return Format.CSV
  if (format == Format.JSON.value):
    return Format.JSON
  if (format == Format.SQL.value):
    return Format.SQL
  
def get_save_path(company: str, year: int, month: int, state: str, format:Format):
  path = PATH['base_folder']
  path = f"{path}/{format.value}"
  file_name = f'{company}_{year}_{month}_{state}.{format.value}'
  return f"{path}/{file_name}"

def build_sql(df:pandas.DataFrame):
  engine = create_engine('sqlite:///:memory:')
  df.to_sql(SQL_FILE_TABLE_NAME, con=engine, if_exists='replace', index=False)
  return engine.execute(f"SELECT * FROM {SQL_FILE_TABLE_NAME}").fetchall()

def df_to_sql_file(df:pandas.DataFrame):
  path = PATH['base_folder']
  path = f'{path}/sql/{SQL_FILE}'
  result = build_sql(df)
  with open(path, 'a') as file:
    file.write(f"INSERT INTO {SQL_FILE_TABLE_NAME} ({', '.join(df.columns)}) VALUES\n")
    for i, row in enumerate(result):
      formatted_values = []
      for value in row:
        if isinstance(value, str):
          new_val = value.replace("'", "''")
          formatted_values.append(f"'{new_val}'")
        elif value is None:
          formatted_values.append('NULL')
        else:
          formatted_values.append(str(value))
      file.write(f"({', '.join(formatted_values)})")
      if i < len(result) - 1:
        file.write(',\n')
      else:
        file.write(';\n\n')
