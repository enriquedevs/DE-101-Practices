from flask import Flask, jsonify
import glob
import json
import csv
import os.path

from common.constants import FOLDER_SEPARATOR, FILE_SEPARATOR, EXTENSION_SEPARATOR, Format
from common.utils import get_uniques, build_prefix

app = Flask(__name__)

@app.route('/', methods=['GET'])
@app.route('/format', methods=['GET'])
@app.route('/format/', methods=['GET'])
def get_index():
  prefix = build_prefix()
  sufix = FOLDER_SEPARATOR

  file_list = glob.glob(f"{prefix}*")
  uniques = get_uniques(prefix, sufix, file_list)

  if len(uniques) == 0:
    return jsonify({}), 404

  return jsonify({
    'format': uniques
  })

@app.route('/format/<file_format>', methods=['GET'])
@app.route('/format/<file_format>/', methods=['GET'])
@app.route('/format/<file_format>/company', methods=['GET'])
@app.route('/format/<file_format>/company/', methods=['GET'])
def get_by_format(file_format):
  prefix = build_prefix(
    file_format=file_format
  )
  sufix = FILE_SEPARATOR

  file_list = glob.glob(f"{prefix}*")
  uniques = get_uniques(prefix, sufix, file_list)

  if len(uniques) == 0:
    return jsonify({}), 404

  return jsonify({
    'format': file_format,
    'company': uniques
  })

@app.route('/format/<file_format>/company/<company>', methods=['GET'])
@app.route('/format/<file_format>/company/<company>/', methods=['GET'])
@app.route('/format/<file_format>/company/<company>/year', methods=['GET'])
@app.route('/format/<file_format>/company/<company>/year/', methods=['GET'])
def get_by_company(file_format, company):
  prefix = build_prefix(
    file_format=file_format,
    company=company
  )
  sufix = FILE_SEPARATOR

  file_list = glob.glob(f"{prefix}*")
  uniques = get_uniques(prefix, sufix, file_list)

  if len(uniques) == 0:
    return jsonify({}), 404

  return jsonify({
    'format': file_format,
    'company': company,
    'year': uniques
  })

@app.route('/format/<file_format>/company/<company>/year/<year>', methods=['GET'])
@app.route('/format/<file_format>/company/<company>/year/<year>/', methods=['GET'])
@app.route('/format/<file_format>/company/<company>/year/<year>/month', methods=['GET'])
@app.route('/format/<file_format>/company/<company>/year/<year>/month/', methods=['GET'])
def get_by_year(file_format, company, year):
  prefix = build_prefix(
    file_format=file_format,
    company=company,
    year=year
  )
  sufix = FILE_SEPARATOR

  file_list = glob.glob(f"{prefix}*")
  uniques = get_uniques(prefix, sufix, file_list)

  if len(uniques) == 0:
    return jsonify({}), 404

  return jsonify({
    'format': file_format,
    'company': company,
    'year': year,
    'month': uniques,
    
  })

@app.route('/format/<file_format>/company/<company>/year/<year>/month/<month>', methods=['GET'])
@app.route('/format/<file_format>/company/<company>/year/<year>/month/<month>/', methods=['GET'])
@app.route('/format/<file_format>/company/<company>/year/<year>/month/<month>/state', methods=['GET'])
@app.route('/format/<file_format>/company/<company>/year/<year>/month/<month>/state/', methods=['GET'])
def get_by_month(file_format, company, year, month):
  prefix = build_prefix(
    file_format=file_format,
    company=company,
    year=year,
    month=month
  )
  sufix = f'{EXTENSION_SEPARATOR}'

  file_list = glob.glob(f"{prefix}*")
  uniques = get_uniques(prefix, sufix, file_list)

  if len(uniques) == 0:
    return jsonify({}), 404

  return jsonify({
    'format': file_format,
    'company': company,
    'year': year,
    'month': month,
    'state': uniques
  })

@app.route('/format/<file_format>/company/<company>/year/<year>/month/<month>/state/<state>', methods=['GET'])
@app.route('/format/<file_format>/company/<company>/year/<year>/month/<month>/state/<state>/', methods=['GET'])
def get_by_state(file_format, company, year, month, state):
  prefix = build_prefix(
    file_format=file_format,
    company=company,
    year=year,
    month=month,
    state=state
  )
  sufix = f'{EXTENSION_SEPARATOR}{file_format}'

  file_path = prefix + sufix

  print(file_path)

  data = []
  if os.path.exists(file_path):
    with open(file_path, 'r') as file:
      if (file_format == Format.JSON.value):
        data = json.load(file)
      else:
        reader = csv.reader(file)
        for row in reader:
          data.append(row)
  else:
    return jsonify({}), 404

  return jsonify({
    'format': file_format,
    'company': company,
    'year': year,
    'month': month,
    'state': state,
    'data': data
  })

@app.route('/format/<file_format>/company/<company>/year/<year>/month/<month>/state/<state>', methods=['DELETE'])
@app.route('/format/<file_format>/company/<company>/year/<year>/month/<month>/state/<state>/', methods=['DELETE'])
def delete_by_state(file_format, company, year, month, state):
  prefix = build_prefix(
    file_format=file_format,
    company=company,
    year=year,
    month=month,
    state=state
  )
  sufix = f'{EXTENSION_SEPARATOR}{file_format}'

  file_path = prefix + sufix
  print(file_path)

  if os.path.exists(file_path):
    os.remove(file_path)

    # Check if last element on the folder then delete
    prefix = build_prefix(file_format=file_format)
    sufix = FILE_SEPARATOR

    file_list = glob.glob(f"{prefix}*")
    if len(file_list) == 0:
      os.rmdir(prefix)
    return jsonify({})
  return 204

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5001)
else:
  app.run(host='0.0.0.0', port=5001)
