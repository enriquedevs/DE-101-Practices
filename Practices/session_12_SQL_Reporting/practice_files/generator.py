import pandas

from common.utils import create_root_dir, get_save_path, decimal_random, PATH
from common.arg_parser import args

START_YEAR = args.start_year
YEAR_RANGE = args.year_range
HDFS = args.hdfs
COMPANIES = args.companies

product_df = pandas.read_csv(PATH['product'])
state_df = pandas.read_csv(PATH['state'])

create_root_dir()

for company in COMPANIES:
  for year in range(YEAR_RANGE):
    curr_year = year + START_YEAR
    for month in range(12):
      curr_month = f'{(month + 1):02d}'
      for state in state_df["state"]:
        file_name = get_save_path(
          company=company,
          year=curr_year,
          month=curr_month,
          state=state,
          hdfs=HDFS
        )
        # insert into df
        product_df['new_price'] = product_df.apply(
            lambda row: round(row['price'] * decimal_random(), 2),
            axis=1
          )
        product_df['new_sales'] = product_df.apply(
            lambda row: round(row['sales'] * decimal_random(), 2),
            axis=1
          )
        product_df['company'] = company
        product_df['year'] = curr_year
        product_df['month'] = curr_month
        product_df['state'] = state

        # new df with only the columns we need
        df = product_df[['name','category','brand','new_price','new_sales','company','year','month','state']].copy()
        df = df.rename(columns={'new_price': 'price', 'new_sales': 'sales'})

        df.to_csv(file_name, index=False)
