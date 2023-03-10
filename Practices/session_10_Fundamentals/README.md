# SQL SCD

In this practice we will create an CDC for a products dataset which is incomplete.

# Practice

Given the queries that you can see in the data below the folder `data`
there is a problem in this data, which is that there is no historical records
of the products. But the business made to get a backup of that table for the
last month of every year since 2015 to 2020.

### Considerations

- Business doesn't have a history logger.
- You need to keep track of the data on every year.
- They will give you the data every january 1st.
- This company's will be called "Company A"

### Technical requirements

- Load the data with a python Script
- The result should be pushed to your database inside the data warehouse.

# Let's do it

## Step 1

First of all we will need to load the data into our dataframe. \
To do so we need to create a python script that uses pandas. \
Use the example in `session_4` to create your python environment.

## Step 2

We need to get the basic parameters for the snowflake connection.

```python
from snowflake.connector import connect

with connect(
    account="<SNOWFLAKE_LOCATOR>",
    user="<SNOWFLAKE_USERNAME>",
    password="<SNOWFLAKE_PASSWORD>",
    database="<SNOWFLAKE_DB>",
    schema="<SNOWFLAKE_DB_SCHEMA>",
    warehouse="<SNOWFLAKE_WAREHOUSE>",
    region="<SNOWFLAKE_AWS_REGION>"
) as connection:
    pass
```

#### SNOWFLAKE_LOCATOR

- This is the parameter that you can get when you log in to snowflake and go to Admin > Accounts. \
    The field that you will need is in the column "Locator"

#### SNOWFLAKE_USERNAME

- The username that you registered in snowflake

#### SNOWFLAKE_PASSWORD

- The password that you used to register in snowflake

#### SNOWFLAKE_DB

- The database that you want to connect and make queries to.

#### SNOWFLAKE_DB_SCHEMA

- The schema in which you want to operate [OPTIONAL]

#### SNOWFLAKE_WAREHOUSE

- Warehouse that you want to use to compute your queries.

#### SNOWFLAKE_AWS_REGION

- in this case for AWS you will need to put the AWS Region in which our snowflake server is located. 
    This information can be found in the same panel as the `SNOWFLAKE_LOCATOR` under the column "REGION.


  
## Step 3

We need to load the data into dataframes, but as we can see we have many files.
So we need to read all of them and do the process for every file in this folder.

``` python
import os
import pandas as pd

list_dir = os.listdir("data") # this will get all the files and directories under the folder data

csv_files = filter(lambda item: item.endswith(".csv")) # Making sure that we are just using the correct file format

for csv_file in csv_files:
    df = pd.read_csv(csv_file)
```

## Step 4

Now that we have the data loaded in our script, we need to make some changes to it:
such as the date in which they were created, or in this case, at least the year.

```python
import os
import pandas as pd

list_dir = os.listdir("company A")  # this will get all the files and directories under the folder company B

csv_files = filter(lambda item: item.endswith(".csv"),
                   list_dir)  # Making sure that we are just using the correct file format

for current_file in csv_files:
    df = pd.read_csv(current_file)
    _, year = current_file.split("_")
    year = year.replace(".csv", "")
    df["valid_for_year"] = year
```

## Step 5

We now have the data with the year that they came from, we need to save it to snowflake
And for that we need to consider a few things:

As it was told before, we need a database, and a table as well, because we need a place to put the data.

- Let's go to snowflake and log in.
- Select the "Data" tab
- In the up-right corner we will see a button "+ Database"
- it should pop up a modal with two fields: "Name" and "Comment" (1.1)
- You can fill it with the information you want, just remember that "Name" should not contain spaces.
- For this exercise let's ust call it "Fundamentals_DB"
- Now push "Create" button, and now we can go to the worksheets (1.2)
- Now in worksheets we will create a new one with the button in the top-right corner 

(1.1 image)\
![1.1.png](resources%2F1.1.png)

(1.2 image)\
![1.2.png](resources%2F1.2.png)

(1.3 image)\
![1.3.png](resources%2F1.3.png)

## Step 6

We now need to create or tables where we will put all of our data.

In your worksheet you will be able to create a new table, but there is one consideration.
As snowflake is a multiple database container (data warehouse), at first it won't have a context
of what are you willing to use, so first of all let's define it.

```snowflake
USE Fundamentals_DB; // or the database you are willing to use
USE WAREHOUSE COMPUTE_WH;  // with this you will select the warehouse 
                           // you will use to compute your query
```

with this two lines you will give snowflake enough context to work.

Now let's go and create the table to be filled.

```snowflake
CREATE TABLE products (
    name varchar(500),
    description varchar(500),
    price FLOAT,
    stock FLOAT
)
```

With this query we will create a table with enough columns for the job.

But don't forget that we need to keep track of the year, so we need to add a new column


```snowflake
CREATE TABLE products (
    name varchar(500),
    description varchar(500),
    price FLOAT,
    stock FLOAT,
    valid_for_year INTEGER
)
```

by the moment we will be able to work with this.

## Step 7

Now let's go on with the python script

first we need to create our connection to snowflake

```python
import os
import pandas as pd

from snowflake.connector import connect

with connect(
        account="<SNOWFLAKE_LOCATOR>",
        user="<SNOWFLAKE_USERNAME>",
        password="<SNOWFLAKE_PASSWORD>",
        database="<SNOWFLAKE_DB>",
        schema="<SNOWFLAKE_DB_SCHEMA>",
        warehouse="<SNOWFLAKE_WAREHOUSE>",
        region="<SNOWFLAKE_AWS_REGION>"
) as connection:
    list_dir = os.listdir("company A")  # this will get all the files and directories under the folder company B

    csv_files = filter(lambda item: item.endswith(".csv"),
                       list_dir)  # Making sure that we are just using the correct file format

    for current_file in csv_files:
        df = pd.read_csv(current_file)
        _, year = current_file.split("_")
        year = year.replace(".csv", "")
        df["valid_for_year"] = year
```

With this we will create our snowflake connection, even if it doesn't do anything by the moment

So by now we know that we don't load anything to snowflake let's create a function that loads your data from the data frame.

```python
from snowflake.connector import SnowflakeConnection


def upload_to_snowflake(connection: SnowflakeConnection, data_frame, table_name):
    with connection.cursor() as cursor:
        query = f"INSERT INTO {table_name} (name, description, price, stock, valid_for_year) VALUES (%s, %s, %s, %s, %s)"
        data = data_frame[['name', 'description', 'price', 'stock', 'valid_for_year']].values.tolist()

        cursor.executemany(query, data)
```

With this you will be able to load your data to snowflake in the main script as the following example:

```python
import os
import pandas as pd

from snowflake.connector import connect

with connect(
        account="<SNOWFLAKE_LOCATOR>",
        user="<SNOWFLAKE_USERNAME>",
        password="<SNOWFLAKE_PASSWORD>",
        database="<SNOWFLAKE_DB>",
        schema="<SNOWFLAKE_DB_SCHEMA>",
        warehouse="<SNOWFLAKE_WAREHOUSE>",
        region="<SNOWFLAKE_AWS_REGION>"
) as connection:
    list_dir = os.listdir("company A")  # this will get all the files and directories under the folder company B

    csv_files = filter(lambda item: item.endswith(".csv"),
                       list_dir)  # Making sure that we are just using the correct file format

    for current_file in csv_files:
        df = pd.read_csv(current_file)
        _, year = current_file.split("_")
        year = year.replace(".csv", "")
        df["valid_for_year"] = year
        upload_to_snowflake(connection, df, "products")
```

# Conclusion

As you can see, we created a CDC (Change Data Capture) that keeps the data from description,
price and stock. this, just by using the "valid_for_year". but if the name of the product changes
we wouldn't be able to know or track it.
 

# HOMEWORK TIME !!!

at this moment this whole script is able to produce a simple CDC in case that anything but the name of the product changes.

But the problem is that there would be a problem if suddenly, Company A decides to send you data for every month or day.
Even, what happens if a product changes its description, or even the name?

use the `homework/generator.py` script to generate enough data for you to do this homework

- try to lose the **least amount** possible of data
- don't modify the script unless it is to fix an error
- You can use the ID column, but if possible try not to use it
- This is an important homework because you will use the result in the session 12 practice