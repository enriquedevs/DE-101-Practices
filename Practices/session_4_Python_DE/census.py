import pandas as pd

# Load the data from the CSV file into a pandas dataframe
df = pd.read_csv("data.csv")

# Calculate the average age
average_age = df["age"].mean()
print("Average age:", average_age)

# Calculate the count of each occupation
occupation_counts = df["occupation"].value_counts()
print("Occupation count:")
print(occupation_counts)

# Calculate the average hours per week
average_hours_per_week = df["hours-per-week"].mean()
print("Average hours per week:", average_hours_per_week)

# Determine the maximum salary
max_salary = df["salary"].value_counts().idxmax()
print("Maximum salary:", max_salary)

# Group the data by occupation and salary
grouped = df.groupby(["occupation", "salary"]).mean()

# Find the occupation with the highest salary
highest_salary = grouped.loc[grouped["age"].idxmax()].name[0]
print("Occupation with highest salary:", highest_salary)

# Find the occupation with the lowest salary
lowest_salary = grouped.loc[grouped["age"].idxmin()].name[0]
print("Occupation with lowest salary:", lowest_salary)