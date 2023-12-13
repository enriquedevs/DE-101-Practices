from airflow.hooks.base import BaseHook

CONN_ID = 'forex_api'
HOST = BaseHook.get_connection(CONN_ID).host
BASE_PATH = '/marclamberti/f45f872dea4dfd3eaa015a4a1af4b39b'
PATH = HOST + BASE_PATH +'/raw/556b22b51b75866e853cf9a949df80a70ea541ce'
ENDPOINTS = {
  'USD': '/api_forex_exchange_usd.json',
  'EUR': '/api_forex_exchange_eur.json'
}
