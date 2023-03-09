import os
import shutil

import pandas as pd
import numpy as np

BASE_DIR = os.getcwd()

START_YEAR = 2015
END_YEAR = 2020

base_folder = "data"
companies = ["A"]

products = pd.read_csv(os.path.join(BASE_DIR, "products.csv"))

prices = products['price']
stocks = products['stock']

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

    for year in range(END_YEAR - START_YEAR + 1):
        for month in range(12):
            random_prices = prices * np.random.uniform(0.8, 1.2, len(prices))
            random_stocks = stocks * np.random.uniform(0.8, 1.5, len(stocks))
            products['price'] = random_prices.round(2)
            products['stock'] = random_stocks.round(2)
            file_name = f'{base_folder}/company {company}/products_{year + START_YEAR}-{(month + 1):02d}.csv'
            products.to_csv(file_name, index=False)
