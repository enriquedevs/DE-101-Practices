import numpy as np

# create a single-dimensional NumPy array
arr1 = np.array([1, 2, 3, 4, 5, 6, 6, 4, 3, 4, 2, 4])

# create a two-dimensional NumPy array
arr2 = np.array([[5, 2, 3], [4, 5, 5], [8, 9, 1]])

# calculate the average value of arr1
avg1 = np.mean(arr1)
print("Average value of arr1:", avg1)

# calculate the minimum value of arr2
min2 = np.min(arr2)
print("Minimum value of arr2:", min2)

# calculate the maximum value of arr2
max2 = np.max(arr2)
print("Maximum value of arr2:", max2)

# calculate the sum of the values in arr2
sum2 = np.sum(arr2)
print("Sum of values in arr2:", sum2)
