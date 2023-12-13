import csv, requests, json
import forex_common.api as f_api
import forex_common.path as f_path

def save2local():
  with open(f'{f_path.DIR}/{f_path.CSV}') as forex_currencies:
    reader = csv.DictReader(forex_currencies, delimiter=',')
    for _, row in enumerate(reader):
      base = row['base']
      with_pairs = row['with_pairs'].split(' ')
      req_path = f"{f_api.PATH}{f_api.ENDPOINTS[base]}"
      indata = requests.get(req_path).json()
      outdata = {'base': base, 'rates': {}, 'last_update': indata['date']}
      for pair in with_pairs:
        outdata['rates'][pair] = indata['rates'][pair]
      with open(f_path.OUT_FILE, 'a') as outfile:
        json.dump(outdata, outfile)
        outfile.write('\n')
