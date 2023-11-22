import requests

from common.constants import HOST

def do_req(path:str, field_res:str):
  url = HOST + path
  response = requests.get(url)
  if response.status_code == 200:
    data = response.json()
    return data[field_res]
  else:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    return []

def do_req_del(path:str):
  url = HOST + path
  response = requests.delete(url)
  if response.status_code == 200 or response.status_code == 204:
    return True
  else:
    print(f"Failed to delete data. Status code: {response.status_code}")
    return False
