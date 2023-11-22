import os
from pathlib import Path
from enum import Enum

BASE_DIR = Path(os.path.dirname(__file__)).parent
BASE_DIR_PARENT = Path(os.path.dirname(__file__)).parent.parent

PATH = {
  'product': f"{BASE_DIR}/data/product.csv",
  'state': f"{BASE_DIR}/data/state.csv",
  'base_folder': f"{BASE_DIR_PARENT}/generated_data"
}

SQL_FILE_TABLE_NAME = 'sales_backup'
SQL_FILE = 'backup.sql'

CREATE_TABLE = '''CREATE TABLE sales_backup (
  name VARCHAR(255),
  category VARCHAR(255),
  brand VARCHAR(255),
  price DECIMAL(10, 2),
  sales DECIMAL(10, 2),
  company VARCHAR(255),
  year INT,
  month VARCHAR(2),
  state VARCHAR(255)
);'''

class Format(Enum):
  CSV = 'csv'
  JSON = 'json'
  SQL = 'sql'
