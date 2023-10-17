import numpy as np

# Load the CSV file into a NumPy array
with open('../census_data.csv') as csvfile:
    data = np.genfromtxt(csvfile, delimiter=',', skip_header=1)


# Extract the hours-per-week and age columns
hours = data[:, 12]  # extracts hours-per-week values on an array
age = data[:, 0]  # extracs age values on an array

# Calculate the average hours-per-week
avg_hours = np.mean(hours)

# Find the maximum and minimum age
max_age = np.max(age)
min_age = np.min(age)
avg_age = np.mean(age)

# Print the results
print("Average hours-per-week:", avg_hours)
print("Maximum age:", max_age)
print("Minimum age:", min_age)
print("Average age:", avg_age)
