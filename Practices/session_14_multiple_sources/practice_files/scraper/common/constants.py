import os
from enum import Enum

HOST = 'http://127.0.0.1:5001'

TABLE_NAME = 'sales_scrapper'

SNOW_CREDS = {
  'user': os.environ['SNOW_USER'],
  'password': os.environ['SNOW_PWD'],
  'account': os.environ['SNOW_ACCOUNT'],
  'warehouse': os.environ['SNOW_WH'],
  'database': os.environ['SNOW_DB'],
  'schema': os.environ['SNOW_SCHEMA']
}

class Format(Enum):
  CSV = 'csv'
  JSON = 'json'

class Path(Enum):
  FORMAT = '/format/'
  COMPANY = '/company/'
  YEAR = '/year/'
  MONTH = '/month/'
  STATE = '/state/'

class Field(Enum):
  FORMAT = 'format'
  COMPANY = 'company'
  YEAR = 'year'
  MONTH = 'month'
  STATE = 'state'
  DATA = 'data'
