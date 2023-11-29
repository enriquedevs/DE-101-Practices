import pandas
import sys

from common.utils import create_root_dir, create_sql_file, get_save_path, decimal_random, get_format, df_to_sql_file
from common.constants import PATH, Format
from common.arg_parser import args

chars = r'/-\|'

YEAR = args.year
COMPANY = args.company
format = get_format(args.format)

product_df = pandas.read_csv(PATH['product'])
state_df = pandas.read_csv(PATH['state'])

create_root_dir(format)

if (args.format == Format.SQL.value): create_sql_file()

for month in range(12):
  curr_month = f'{(month + 1):02d}'
  sys.stdout.write(f'\rLoading... {chars[month % len(chars)]}')
  sys.stdout.flush()
  for state in state_df["state"]:
    file_name = get_save_path(
      company=COMPANY,
      year=YEAR,
      month=curr_month,
      state=state,
      format=format
    )
    product_df['new_price'] = product_df.apply(
        lambda row: round(row['price'] * decimal_random(), 2),
        axis=1
      )
    product_df['new_sales'] = product_df.apply(
        lambda row: round(row['sales'] * decimal_random(), 2),
        axis=1
      )

    if (format.value == Format.SQL.value):
        product_df['company'] = COMPANY
        product_df['year'] = YEAR
        product_df['month'] = curr_month
        product_df['state'] = state

        df = product_df[['name','category','brand','new_price','new_sales','company','year','month','state']].copy()
        df = df.rename(columns={'new_price': 'price', 'new_sales': 'sales'})
        df_to_sql_file(df)
    else: # CSV & JSON
      df = product_df[['name','category','brand','new_price','new_sales']].copy()
      df = df.rename(columns={'new_price': 'price', 'new_sales': 'sales'})

      if (format.value == Format.CSV.value):
        df.to_csv(file_name, index=False)
      else: # JSON
        df.to_json(file_name, orient="records")

sys.stdout.write('\rDone!       \n')
