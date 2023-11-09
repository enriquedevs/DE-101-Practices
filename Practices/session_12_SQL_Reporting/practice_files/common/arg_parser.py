import argparse

parser = argparse.ArgumentParser(description='CSV Product Generator')
parser.add_argument('-hd', '--hdfs', help='folders in hdfs style', action='store_true')
parser.add_argument('-y', '--start_year', type=int, help='folder starting year', default=2015)
parser.add_argument('-r', '--year_range', type=int, help='years to generate data, minimum 1', default=2)
parser.add_argument('-c', '--companies', nargs='+', help='custom companies list, use space to separate values: mazda toyota chevrolet', default=["A", "B"])

args = parser.parse_args()

print(f"""#####PARAMETERS####
hdfs={args.hdfs}
start_year={args.start_year}
year_range={args.year_range}
companies={args.companies}
###################""")
