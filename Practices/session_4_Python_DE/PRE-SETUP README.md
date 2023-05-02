

## Step 1

### Python for Data Engineering

Python is a popular programming language for data engineering due to several reasons:

+ **Easy-to-learn and intuitive syntax**: Python's syntax is straightforward and easy to learn, making it an ideal language for beginners. The code is also easy to read and write, making it more efficient for data engineers to work with complex data pipelines.
+ **Wide range of libraries and frameworks**: Python has a large and growing collection of open-source libraries and frameworks, specifically designed for data engineering tasks. These libraries include Pandas, Numpy, Scikit-learn, TensorFlow, PyTorch, Apache Spark, and many more.
+ **Versatility**: Python is a versatile language that can be used for a wide range of tasks, from data processing and analysis to machine learning and data visualization. This versatility makes it an ideal language for data engineers who need to work with a variety of tools and technologies.
+ **Integration with big data technologies**: Python can be used to integrate with big data technologies like Hadoop, Spark, and Hive. This makes it easy for data engineers to work with large data sets, implement data processing workflows, and create scalable data pipelines.
+ **Community support**: Python has a large and active community of developers and data scientists who contribute to the development of libraries and frameworks. The community provides extensive support, resources, and documentation, making it easy for data engineers to find solutions to their problems.

![img](documentation_images/python-de.jpg)

### Python Virtual Environment
**A virtual environment is a self-contained Python environment that allows you to install and run packages separately from your main Python installation. This is especially useful for projects that have different package requirements.**

![img](documentation_images/pyenv.png)

First, we are going to set up a virtual environment in Python, you will need to use the following commands:

```
python -m venv myenv
source myenv/bin/activate
```

* **'python -m venv myenv'** - This command creates a virtual environment with the name "myenv" using the venv module in Python. A virtual environment allows you to isolate the dependencies for your project from the rest of your system, making it easier to manage different versions of libraries for different projects.

* **'source myenv/bin/activate'** - This command activates the virtual environment "myenv". When a virtual environment is activated, any packages you install using pip will be installed in that environment, rather than in your system Python installation. This helps ensure that your project has access to the correct version of libraries, without affecting other projects that may have different requirements.

## Step 2

Now let's install numpy and pandas libraries with following command:

```
pip install numpy pandas
```

### Numpy
**NumPy is a library for the Python programming language that provides support for arrays and matrices. It is a fundamental library for scientific computing with Python, including support for a wide variety of mathematical and statistical operations. The main feature of NumPy is its N-dimensional array object, which allows you to perform operations on arrays of any size and shape, including element-wise operations, matrix multiplication, and basic linear algebra.**

![img](documentation_images/numpy.png)

### Pandas
**pandas is a library for the Python programming language that provides data structures and functions needed for data analysis and data manipulation. It is particularly well-suited for working with labeled, tabular data in a way that is intuitive and easy to understand. The main data structure in pandas is the DataFrame, which is a two-dimensional table with labeled rows and columns. With pandas, you can perform operations on the data, such as filtering, grouping, aggregating, and transforming, with ease. Additionally, pandas provides built-in support for working with data from a variety of sources, including CSV, Excel, SQL databases, and more.**

![img](documentation_images/dataframe.png)

