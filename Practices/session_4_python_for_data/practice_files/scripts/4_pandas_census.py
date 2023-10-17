import pandas as pd

# read the CSV file into a pandas DataFrame
df = pd.read_csv('../census_data.csv')

# calculate the average hours-per-week
avg_hours = df['hours-per-week'].mean()
print('Average hours-per-week:', avg_hours)

# calculate the minimum and maximum age
min_age = df['age'].min()
max_age = df['age'].max()
print('Minimum age:', min_age)
print('Maximum age:', max_age)

# create a new DataFrame with the specified columns
new_df = df[['age', 'education', 'native-country', 'salary']]

# save the new DataFrame to a CSV file
new_df.to_csv('census_demographics.csv', index=False)
print('DataFrame saved to census_demographics.csv')

