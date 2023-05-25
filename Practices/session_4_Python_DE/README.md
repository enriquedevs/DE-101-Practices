# Python for Data Engineering

In this practice we will develop and use a Python script to process data by using Data Engineering libraries such as Numpy and Pandas

![Docker-Python](documentation_images/numpy-pandas.png)

### Prerequisites
* [Install Python on local machine](https://www.python.org/downloads/) 
* [pre-setup](PRE-SETUP%20README.md)

### What You Will Learn
- Process data on a Python Script
- Usage of Numpy Library
- Usage of Pandas Library

# Practice

You are working on a Census Company, and they asking you to provide insights of the census data made on the population.

The company provides you a census data on csv file and they requested you to gather statistics and information from it.

![img](documentation_images/census.png)


### Requirements
* Create a Python Script to process the csv file which contains following census data from people:
  * **age:** Age of the person.
  * **workclass:** Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked.
  * **education:** Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool.
  * **marital-status:** Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse.
  * **occupation:** Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces.
  * **relationship:** Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried.
  * **race:** White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black.
  * **sex:** Female, Male.
  * **hours-per-week:** Weekly working hours.
  * **native-country:** United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands.
  * **salary:** >50K,<=50K
* Obtain requested information of the steps when processing the file

# Let's do it!

## Step 3
### Numpy Arrays
First let's create a python script to start using numpy arrays.

To do so, follow to the python file named [numpy_example.py](src/numpy_example.py)

The code creates following numpy arrays:
* arr1: It's a single dimension array
* arr2: It's a bi-dimensional array

And with the functions (sum, max, min, mean) will be obtained statistics data from the arrays.

Here are some most commons functions on numpy:
+ **np.array()**: Creates a NumPy array from a Python list or other iterable.
+ **np.arange()**: Creates a NumPy array with evenly spaced values between a start and end point.
+ **np.zeros()**: Creates a NumPy array of all zeros with a given shape.
+ **np.ones()**: Creates a NumPy array of all ones with a given shape.
+ **np.linspace()**: Creates a NumPy array with a specified number of evenly spaced values between a start and end point.
+ **np.reshape()**: Reshapes a NumPy array to a specified shape.
+ **np.concatenate()**: Concatenates two or more NumPy arrays along a specified axis.
+ **np.mean()**: Calculates the mean of a NumPy array.
+ **np.median()**: Calculates the median of a NumPy array.
+ **np.var()**: Calculates the variance of a NumPy array.
+ **np.std()**: Calculates the standard deviation of a NumPy array.
+ **np.min()**: Finds the minimum value of a NumPy array.
+ **np.max()**: Finds the maximum value of a NumPy array.
+ **np.argmin()**: Finds the index of the minimum value in a NumPy array.
+ **np.argmax()**: Finds the index of the maximum value in a NumPy array.
+ **np.sort()**: Sorts the values in a NumPy array.
+ **np.unique()**: Finds the unique values in a NumPy array.
+ **np.dot()**: Computes the dot product of two NumPy arrays.
+ **np.transpose()**: Transposes a NumPy array.
+ **np.random()**: Generates random numbers or arrays in a NumPy array.

Now let's run this file on the terminal inside our docker container using:
```
python numpy_example.py
```

## Step 4
### Reading Data with Numpy

Now we will use the CSV data source to read the data from it by using numpy.

Let's follow to the python file named [numpy_census.py](src/numpy_census.py)

In this example, we use the NumPy **genfromtxt()** function to load the given CSV file into a NumPy array. We then extract the hours-per-week, and age columns from the array and use various NumPy functions to perform calculations on these columns, such as calculating the average hours-per-week, and finding the maximum, minimum and average age.

As note:

+ In **data[:, 12]**, the colon **:** before the comma specifies that we want to select all rows of the data array.  
The number **12** after the comma specifies that we want to select the 12th column of the data array.  
So **data[:, 12]** selects all rows and the 12th column of the data array, which corresponds to the **"hours-per-week"** column in the given CSV file.

To run this file, do the following command:

```
python numpy_census.py
```

## Step 5
### Using Pandas Dataframes

Pandas dataframes are a two-dimensional data structure that allows you to store and manipulate tabular data. It's like a "table" data structure on Python.

Let's follow to the python file named [pandas_example.py](src/pandas_example.py)

In this example, we create a sample DataFrame using a Python dictionary and the Pandas DataFrame() constructor. We then perform some simple operations on the DataFrame, such as calculating the average salary, finding the maximum and minimum age, and using the **apply()** method to create a new column that has the sum of two existing columns.

The **apply()** method takes a function as an argument and applies that function to each row or column of the DataFrame. In this example, we use a lambda function to add the "Salary" and "Experience" columns together and create a new column called "Salary plus Experience".

Here are some most commons functions on Pandas Dataframes:
+ **pd.DataFrame()**: Creates a new Pandas DataFrame from a Python dictionary, list, or other data structure.
+ **df.head()**: Returns the first n rows of a DataFrame, where n is the argument passed to the function (defaults to 5).
+ **df.tail()**: Returns the last n rows of a DataFrame, where n is the argument passed to the function (defaults to 5).
+ **df.shape**: Returns a tuple with the number of rows and columns in a DataFrame.
+ **df.columns**: Returns a list of column names in a DataFrame.
+ **df.dtypes**: Returns a Series with the data type of each column in a DataFrame.
+ **df.describe()**: Generates a summary of descriptive statistics for the columns of a DataFrame, such as count, mean, standard deviation, minimum, maximum, and quartiles.
+ **df.info()**: Provides a concise summary of a DataFrame, including the number of non-null values, data types, and memory usage.
+ **df.isnull()**: Returns a DataFrame with the same shape as the original, where each element is a Boolean value indicating whether it is a null value (i.e., NaN).
+ **df.dropna()**: Returns a new DataFrame with all rows that contain null values removed.
+ **df.fillna()**: Returns a new DataFrame with all null values filled with a specified value or method.
+ **df.sort_values()**: Sorts a DataFrame by one or more columns, either in ascending or descending order.
+ **df.groupby()**: Groups a DataFrame by one or more columns and returns a DataFrameGroupBy object that can be used to perform further operations.
+ **df.apply()**: Applies a function to each row or column of a DataFrame.
+ **df.merge()**: Combines two or more DataFrames into a single DataFrame based on a common key or index.

Now let's run this file on the terminal with:
```
python pandas_example.py
```

## Step 6
### Reading and Writing Data with Pandas Dataframes
Now we will use the CSV data source to read the data from it by using pandas dataframes.

Let's follow to the python file named [pandas_census.py](src/pandas_census.py)

In this script, we first read the **census_data.csv** file into a Pandas DataFrame using the **read_csv()** function. We then calculate the average hours-per-week, minimum and maximum age, and most common occupation using various DataFrame functions.

Then the script creates a new DataFrame with only the columns we are interested in (age, education, native-country, and salary) and save it to a new CSV file using the **to_csv()** function

Now let's run this file with the following command:

```
python pandas_census.py
```

And a new **'census_demographics.csv'** file will be created on current directory.

## HOMEWORK TIME !!!

**By using same pandas_census.py, modify the code to store on csv file the following:**

+ **age**: age
+ **education**: education
+ **native-country**: native-country
+ **salary**: salary
+ **age-is-above-21**: this column will contain 'true' in case the age is above 21, if not, then will have 'false'
+ **education-salary**: this column will have 'A person with {education} is having {salary}', where {education} refers to row's education, and {salary} refers to row's salary.

# Conclusion

This course has covered the basics of Numpy and Pandas, including setting up a virtual environment, reading in data, and performing transformations on that data. With these tools and techniques, you can begin working with large datasets and performing data analysis in Python.