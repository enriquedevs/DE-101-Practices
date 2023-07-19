import pandas as pd

# Create a sample DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
        'Age': [25, 30, 35, 40, 45],
        'Salary': [50000, 60000, 70000, 80000, 90000],
        'Experience': [3, 5, 7, 9, 11]}
#print(data)

df = pd.DataFrame(data)

# Calculate the average salary
avg_salary = df['Salary'].mean()

# Find the maximum and minimum age
max_age = df['Age'].max()
min_age = df['Age'].min()

def myfunc(row):
    return row['Salary'] + row['Experience']


# Use apply() to create a new columns ('Salary plus Experience' and 'Name with Age')
df['Salary plus Experience'] = df.apply(myfunc, axis=1)
df['Name with Age'] = df.apply(lambda row: f"{row['Name']} is having {row['Age']} years old", axis=1)

print(df)

'''
# Print the results
print("Average salary:", avg_salary)
print("Maximum age:", max_age)
print("Minimum age:", min_age)
print(df)
'''

