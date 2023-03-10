import os
import shutil

import pandas as pd
import numpy as np

BASE_DIR = os.getcwd()

START_YEAR = 2015
END_YEAR = 2020

base_folder = "data"
companies = ["B"]

products = pd.read_csv(os.path.join(BASE_DIR, "products.csv"))
states_csv = pd.read_csv(os.path.join(BASE_DIR, "states.csv"))
states = states_csv["state"]
prices = products['price']
sales = products['sales']

try:
    os.mkdir(base_folder)
except:
    shutil.rmtree(base_folder)
    os.mkdir(base_folder)

for company in companies:
    company_path = f"{os.path.join(base_folder, f'company {company}')}"
    try:
        os.mkdir(company_path)
    except:
        shutil.rmtree(company_path)
        os.mkdir(company_path)

    for state in states:
        for year in range(END_YEAR - START_YEAR + 1):
            for month in range(12):
                random_prices = prices * np.random.uniform(0.8, 1.2, len(prices))
                random_sales = sales * np.random.uniform(0.8, 1.7, len(sales))
                products['price'] = random_prices.round(2)
                products['sales'] = random_sales.round(0)
                file_name = f'{base_folder}/company {company}/products_{state}_{year + START_YEAR}-{(month + 1):02d}.csv'
                products.to_csv(file_name, index=False)
