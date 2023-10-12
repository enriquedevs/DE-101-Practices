# Python for Data Engineering

In this practice we will develop and use a Python script to process data by using Data Engineering libraries such as Numpy and Pandas

![Docker-Python](documentation_images/numpy-pandas.png)

## Prerequisites

* [Pre Setup][pre_setup]
* [Python Install on local machine][python]

## What You Will Learn

* Process data on a Python Script
* Usage of Numpy Library
* Usage of Pandas Library

## Practice

You are working on a Census Company, and they asking you to provide insights of the census data made on the population.

The company provides you a census data on csv file and they requested you to gather statistics and information from it.

![img](documentation_images/census.png)

### Requirements

Create a Python Script to process the csv file which contains following census data from people:

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

### Step 1: Numpy Arrays

First let's create a python script to start using numpy arrays.

To do so, follow to the python file named [numpy_example.py](src/numpy_example.py)

The code creates following numpy arrays:

* arr1: It's a single dimension array
* arr2: It's a bi-dimensional array

And with the functions (sum, max, min, mean) will be obtained statistics data from the arrays.

Here are some most commons functions on numpy:

* **np.array()**: Creates a NumPy array from a Python list or other iterable.
* **np.arange()**: Creates a NumPy array with evenly spaced values between a start and end point.
* **np.zeros()**: Creates a NumPy array of all zeros with a given shape.
* **np.ones()**: Creates a NumPy array of all ones with a given shape.
* **np.linspace()**: Creates a NumPy array with a specified number of evenly spaced values between a start and end point.
* **np.reshape()**: Reshapes a NumPy array to a specified shape.
* **np.concatenate()**: Concatenates two or more NumPy arrays along a specified axis.
* **np.mean()**: Calculates the mean of a NumPy array.
* **np.median()**: Calculates the median of a NumPy array.
* **np.var()**: Calculates the variance of a NumPy array.
* **np.std()**: Calculates the standard deviation of a NumPy array.
* **np.min()**: Finds the minimum value of a NumPy array.
* **np.max()**: Finds the maximum value of a NumPy array.
* **np.argmin()**: Finds the index of the minimum value in a NumPy array.
* **np.argmax()**: Finds the index of the maximum value in a NumPy array.
* **np.sort()**: Sorts the values in a NumPy array.
* **np.unique()**: Finds the unique values in a NumPy array.
* **np.dot()**: Computes the dot product of two NumPy arrays.
* **np.transpose()**: Transposes a NumPy array.
* **np.random()**: Generates random numbers or arrays in a NumPy array.

Now let's run this file on the terminal inside our docker container using:

```sh
python numpy_example.py
```

### Step 2: eading Data with Numpy

Now we will use the CSV data source to read the data from it by using numpy.

Let's follow to the python file named [numpy_census.py](src/numpy_census.py)

In this example, we use the NumPy **genfromtxt()** function to load the given CSV file into a NumPy array. We then extract the hours-per-week, and age columns from the array and use various NumPy functions to perform calculations on these columns, such as calculating the average hours-per-week, and finding the maximum, minimum and average age.

>**Note**:
>
>In **data[:, 12]**, the colon **:** before the comma specifies that we want to select all rows of the data array.  
>
>The number **12** after the comma specifies that we want to select the 12th column of the data array.  
>
>So **data[:, 12]** selects all rows and the 12th column of the data array, which corresponds to the **"hours-per-week"** column in the given CSV file.

To run this file, do the following command:

```sh
python numpy_census.py
```

### Step 3: Using Pandas Dataframes

Pandas dataframes are a two-dimensional data structure that allows you to store and manipulate tabular data. It's like a "table" data structure on Python.

Let's follow to the python file named [pandas_example.py](src/pandas_example.py)

In this example, we create a sample DataFrame using a Python dictionary and the Pandas DataFrame() constructor. We then perform some simple operations on the DataFrame, such as calculating the average salary, finding the maximum and minimum age, and using the **apply()** method to create a new column that has the sum of two existing columns.

The **apply()** method takes a function as an argument and applies that function to each row or column of the DataFrame. In this example, we use a lambda function to add the "Salary" and "Experience" columns together and create a new column called "Salary plus Experience".

Here are some most commons functions on Pandas Dataframes:

* **pd.DataFrame()**: Creates a new Pandas DataFrame from a Python dictionary, list, or other data structure.
* **df.head()**: Returns the first n rows of a DataFrame, where n is the argument passed to the function (defaults to 5).
* **df.tail()**: Returns the last n rows of a DataFrame, where n is the argument passed to the function (defaults to 5).
* **df.shape**: Returns a tuple with the number of rows and columns in a DataFrame.
* **df.columns**: Returns a list of column names in a DataFrame.
* **df.dtypes**: Returns a Series with the data type of each column in a DataFrame.
* **df.describe()**: Generates a summary of descriptive statistics for the columns of a DataFrame, such as count, mean, standard deviation, minimum, maximum, and quartiles.
* **df.info()**: Provides a concise summary of a DataFrame, including the number of non-null values, data types, and memory usage.
* **df.isnull()**: Returns a DataFrame with the same shape as the original, where each element is a Boolean value indicating whether it is a null value (i.e., NaN).
* **df.dropna()**: Returns a new DataFrame with all rows that contain null values removed.
* **df.fillna()**: Returns a new DataFrame with all null values filled with a specified value or method.
* **df.sort_values()**: Sorts a DataFrame by one or more columns, either in ascending or descending order.
* **df.groupby()**: Groups a DataFrame by one or more columns and returns a DataFrameGroupBy object that can be used to perform further operations.
* **df.apply()**: Applies a function to each row or column of a DataFrame.
* **df.merge()**: Combines two or more DataFrames into a single DataFrame based on a common key or index.

Now let's run this file on the terminal with:

```sh
python pandas_example.py
```

### Step 4: Reading and Writing Data with Pandas Dataframes

Now we will use the CSV data source to read the data from it by using pandas dataframes.

Let's follow to the python file named [pandas_census.py](src/pandas_census.py)

In this script, we first read the **census_data.csv** file into a Pandas DataFrame using the **read_csv()** function. We then calculate the average hours-per-week, minimum and maximum age, and most common occupation using various DataFrame functions.

Then the script creates a new DataFrame with only the columns we are interested in (age, education, native-country, and salary) and save it to a new CSV file using the **to_csv()** function

Now let's run this file with the following command:

```sh
python pandas_census.py
```

And a new **'census_demographics.csv'** file will be created on current directory.

## HOMEWORK TIME

**By using same pandas_census.py, modify the code to store on csv file the following:**

* **age**: age
* **education**: education
* **native-country**: native-country
* **salary**: salary
* **age-is-above-21**: this column will contain 'true' in case the age is above 21, if not, then will have 'false'
* **education-salary**: this column will have 'A person with {education} is having {salary}', where {education} refers to row's education, and {salary} refers to row's salary.

## Conclusion

In this practice we view the basics of **Numpy** and **Pandas**.

These tools are one of the most common for data engineering tasks, including data processing, analysis, and manipulation.

## Still curious

>Do you wnat to know more about Numpy and Pandas?

* Why is Numpy so popular?

1. Array Operations: Numpy base object is called **ndarray**, this stands for *nth dimension Array*, this allows operations with the same generic object, making processing simpler.
2. Low level coding: Under the hood **ndarray** along with other functions, are implemented in C and Fortran, which allows faster operations than Python
3. Wide operation range: Numpy implements a large set of methods (operations), giving most of the time the need of not requiring other tools for data processing
4. Interoperability: Usually you will find Numpy related libraries for integration with other libraries, such as SciPy, MatplobLib, Pandas...
5. Open source: Community is always on top and you can make your own modiffications

* You may also want to consider some disadvantages:

1. Limited Support for Non-Numerical Data: NumPy is primarily designed for numerical computations. It is less suitable for handling non-numeric data or structured data like strings, dates, and categorical variables.
2. Single Data Type: NumPy arrays are homogeneous, meaning all elements must have the same data type. This can be limiting when working with mixed data types or structured data.
3. Memory Usage: NumPy can consume a significant amount of memory, especially when dealing with large arrays. For certain memory-constrained applications, this can be a drawback.
4. Not Built for Data Manipulation: While NumPy provides basic array manipulation capabilities, it lacks some of the advanced data manipulation features available in libraries like Pandas.
5. Less User-Friendly for Beginners: NumPy's syntax can be less intuitive for beginners.

* Why is Pandas so popular?

1. Tabular Data Handling: Pandas provides easy-to-use data structures like DataFrames and Series, which are well-suited for working with structured, tabular data.
2. Data Cleaning: Pandas offers robust tools for data cleaning and preprocessing, including handling missing values, data imputation, and removing duplicates.
3. Data Transformation: You can easily reshape and transform data using operations like merging, pivoting, and aggregating, making it ideal for data wrangling.
4. Data Exploration: Pandas allows for quick data exploration and summary statistics, helping users gain insights into their datasets.
5. Time Series Analysis: It has extensive support for time series data, including date and time parsing, resampling, and rolling calculations.
6. Integration with Other Libraries: Pandas seamlessly integrates with other Python libraries, such as NumPy, Matplotlib, and Scikit-Learn, creating a powerful ecosystem for data analysis and machine learning.
7. I/O Operations: Pandas supports a wide range of file formats for reading and writing data, including CSV, Excel, SQL databases, and JSON.
8. Customization: You can customize and extend Pandas' functionality by creating custom functions and applying them to your data.

* You may also want to consider some disadvantages:

1. Memory Usage: Pandas can be memory-intensive, especially when working with large datasets. It may not be suitable for very large datasets that do not fit into memory.
2. Learning Curve: While Pandas is powerful, its syntax and functionality can be complex for beginners. It may take some time to become proficient in using the library effectively.
3. Performance: Some operations in Pandas can be slower than equivalent operations in low-level languages like C++. For highly performance-critical tasks, specialized libraries may be more suitable.
4. Limited Non-Tabular Data Handling: Pandas is designed for tabular data, so it may not be the best choice for handling non-tabular data or unstructured data.
5. Compatibility: Minor version updates of Pandas can sometimes lead to compatibility issues with existing code and dependencies.
6. Parallel Processing: Pandas lacks built-in support for parallel processing, which can be a limitation when working with large datasets that could benefit from parallelization.
7. Global State: Pandas modifies global settings, and users may encounter issues when working with multiple Pandas-based projects in the same environment.

>What alternatives exists to Numpy and Pandas?
>
>In what scenarios we want to use those alternatives?

Find more information here:

* [What is Numpy used for in Python][numpy_uses_python]
* [Numpy: Getting started][numpy_docs]
* [When not to use Numpy][no_use_numpy]

* [Pandas: Docs][pandas_docs]
* [Benchmark: Pandas Alternatives][pandas_alt]

## Links

* [Pre Setup][pre_setup]
* [Python Install][python]

* [What is Numpy used for in Python][numpy_uses_python]
* [Numpy: Getting started][numpy_docs]
* [When not to use Numpy][no_use_numpy]

* [Pandas: Docs][pandas_docs]
* [Benchmark: Pandas Alternatives][pandas_alt]

[pre_setup]: pre-setup%20README.md

[python]: https://www.python.org/downloads/
[numpy_uses_python]: https://www.activestate.com/resources/quick-reads/what-is-numpy-used-for-in-python/
[numpy_docs]: https://numpy.org/doc/stable/user/absolute_beginners.html
[no_use_numpy]: https://medium.com/@abhi16.2007/when-i-should-not-use-numpy-1e00aafb231b
[pandas_docs]: https://pandas.pydata.org/docs/ç
[pandas_alt]: https://www.datacamp.com/tutorial/benchmarking-high-performance-pandas-alternatives
