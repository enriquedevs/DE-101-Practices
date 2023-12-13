from airflow.hooks.base import BaseHook

CONN_ID = 'forex_path'
DIR = BaseHook.get_connection(CONN_ID).extra_dejson['path']
CSV = 'forex_currencies.csv'

OUT_FILE = DIR + '/forex_rates.json'
