import pandas, sys

from common.constants import Format, Path, Field
from common.utils import do_req, do_req_del
from common.snow import handle_json, handle_csv

FORMATS = [Format.CSV.value, Format.JSON.value]
chars = r'/-\|'

def scrape_paths():
  df = pandas.DataFrame([], columns=["format", "company", "year", "month", "state", 'uri'])
  for scr_format in FORMATS:
    # print(scr_format)
    url_format = f"{Path.FORMAT.value}{scr_format}"
    companies = do_req(url_format, Field.COMPANY.value)
    # print(companies)

    for company in companies:
      url_year = f"{url_format}{Path.COMPANY.value}{company}"
      years = do_req(url_year, Field.YEAR.value)
      # print(years)

      for year in years:
        url_month = f"{url_year}{Path.YEAR.value}{year}"
        months = do_req(url_month, Field.MONTH.value)
        # print(months)

        for month in months:
          url_state = f"{url_month}{Path.MONTH.value}{month}"
          states = do_req(url_state, Field.STATE.value)
          # print(states)

          for state in states:
            url_data = f"{url_state}{Path.STATE.value}{state}"
            new_row = {
              'format': scr_format,
              'company': company,
              'year': year,
              'month': month,
              'state': state,
              'uri': url_data
            }
            df.loc[len(df)] = new_row
  return df

def scrape_data(df: pandas.DataFrame):
  for i, row in df.iterrows():
    sys.stdout.write(f'\rLoading... {chars[i % len(chars)]}')
    sys.stdout.flush()
    data = do_req(row['uri'], Field.DATA.value)
    if Format.JSON.value == row['format']:
      handle_json(data, row['company'], row['year'], row['month'], row['state'])
    elif Format.CSV.value == row['format']:
      handle_csv(data, row['company'], row['year'], row['month'], row['state'])
    do_req_del(row['uri'])

df = scrape_paths()
scrape_data(df)

sys.stdout.write('\rDone!       \n')
