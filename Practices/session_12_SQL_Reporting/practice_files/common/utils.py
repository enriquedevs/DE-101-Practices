import os
import shutil
import numpy
import pandas
from pathlib import Path

rng = numpy.random.default_rng()
# Returns a random between 0 and 1.999...
def decimal_random():
  ret = rng.integers(low=0,high=2) + rng.random()
  return ret

BASE_DIR = Path(os.path.dirname(__file__)).parent
PATH = {
  'product': f"{BASE_DIR}/data/product.csv",
  'state': f"{BASE_DIR}/data/state.csv",
  'base_folder': f"{BASE_DIR}/generated_data"
}

def create_root_dir():
  try:
    os.mkdir(PATH['base_folder'])
  except:
    shutil.rmtree(PATH['base_folder'])
    os.mkdir(PATH['base_folder'])

def create_dir(path: str):
  try:
    os.mkdir(path)
  except:
    pass

def get_save_path(company: str, year: int, month: int, state: str, hdfs=False):
  path = PATH['base_folder']
  if (hdfs):
    path = f"{path}/company={company}"
    create_dir(path=path)
    path = f"{path}/year={year}"
    create_dir(path=path)
    path = f"{path}/month={month}"
    create_dir(path=path)
    path = f"{path}/state={state}"
    create_dir(path=path)
  file_name = f'{company}_{year}_{month}_{state}.csv'
  return f"{path}/{file_name}"
