import argparse
import sys
from common.constants import Format

parser = argparse.ArgumentParser(description='CSV Product Generator')
parser.add_argument('-y', '--year', type=int, help='year', default=2023)
parser.add_argument('-c', '--company', type=str, help='company name', default="MyCompany")
parser.add_argument('-f', '--format', type=str, help='json, csv, sql', default='csv')

args = parser.parse_args()

print(f"""#####PARAMETERS####
year={args.year}
company={args.company}
format={args.format}
###################""")

if (not (args.format == Format.CSV.value or args.format == Format.JSON.value or args.format == Format.SQL.value)):
  print('Invalid format')
  sys.exit(1)
