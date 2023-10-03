# SQL CDC

In this practice we will create an CDC for a products dataset which is incomplete.

## Practice

Use the backup files in the [data][data_folder] to restore the database.

### Considerations

* The products may have changed over the years; so you can ignore the id column in the backups as it's just an enumerator
* Business doesn't have a history logger (The backup folder is the only information available)
* You need to keep track of the data on every year.
* They will give you the data every january 1st.

### Technical requirements

* Load the data with a python Script
* The result should be pushed to your database inside the data warehouse.

## Step 1 - pyenv

First of all we will need to load the data into our dataframe. To do so we need to create a python script that uses pandas.

* Use the example in [session 4][py_env] to create your python environment.

## Step 2 - Python connection

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

* SNOWFLAKE_LOCATOR
  
  This is the parameter that you can get when you log in to snowflake and go to Admin > Accounts. \
  The field that you will need is in the column "Locator"

* SNOWFLAKE_USERNAME

  The username that you registered in snowflake

* SNOWFLAKE_PASSWORD

  The password that you used to register in snowflake

* SNOWFLAKE_DB

  The database that you want to connect and make queries to.

* SNOWFLAKE_DB_SCHEMA

  The schema in which you want to operate [OPTIONAL]

* SNOWFLAKE_WAREHOUSE

  Warehouse that you want to use to compute your queries.

* SNOWFLAKE_AWS_REGION

  In this case for AWS you will need to put the AWS Region in which our snowflake server is located. \
  This information can be found in the same panel as the `SNOWFLAKE_LOCATOR` under the column "REGION.

## Step 3 - Loading into Dataframes

We need to load the data into dataframes, but as we can see we have many files. \
So we need to read all of them and do the process for every file in this folder.

``` python
import os
import pandas as pd

list_dir = os.listdir("data") # this will get all the files and directories under the folder data

csv_files = filter(lambda item: item.endswith(".csv")) # Making sure that we are just using the correct file format

for csv_file in csv_files:
    df = pd.read_csv(f'./data/{csv_file}')
```

## Step 4 - Dataframe modifications

Now that we have the data loaded in our script, we need to make some changes to it: \
Such as the date in which they were created, or in this case, at least the year.

```python
for current_file in csv_files:
    df = pd.read_csv(f'./data/{current_file}')
    _, year = current_file.split("_")
    year = year.replace(".csv", "")
    df["valid_for_year"] = year
```

## Step 5 - Snowflake Setup

We now have the data with the year that they came from, we need to save it to snowflake
And for that we need to consider a few things:

As it was told before, we need a database, and a table as well, because we need a place to put the data.

* Let's go to snowflake and log in.
* Select the "Data" tab
* In the up-right corner we will see a button "+ Database"
* it should pop up a modal with two fields: "Name" and "Comment" (1.1)
* You can fill it with the information you want, just remember that "Name" should not contain spaces.
* For this exercise let's ust call it "Fundamentals_DB"
* Now push "Create" button, and now we can go to the worksheets (1.2)
* Now in worksheets we will create a new one with the button in the top-right corner

![1.1.png](resources%2F1.1.png)
Image 1.1

![1.2.png](resources%2F1.2.png)
Image 1.2

![1.3.png](resources%2F1.3.png)
Image 1.3

## Step 6 - Creating Tables

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

## Step 7 - Connecting and dumping data into snowflake

Now let's go on with the python script

first we need to create our connection to snowflake

```py
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
    list_dir = os.listdir("data")  # this will get all the files and directories

    csv_files = filter(lambda item: item.endswith(".csv"),
                       list_dir)  # Making sure that we are just using the correct file format

    for current_file in csv_files:
        df = pd.read_csv(f'./data/{current_file}')
        _, year = current_file.split("_")
        year = year.replace(".csv", "")
        df["valid_for_year"] = year
```

With this we will create our snowflake connection, even if it doesn't do anything by the moment

So by now we know that we don't load anything to snowflake let's create a function that loads your data from the data frame.

```py
from snowflake.connector import SnowflakeConnection


def upload_to_snowflake(connection: SnowflakeConnection, data_frame, table_name):
    with connection.cursor() as cursor:
        query = f"INSERT INTO {table_name} (name, description, price, stock, valid_for_year) VALUES (%s, %s, %s, %s, %s)"
        data = data_frame[['name', 'description', 'price', 'stock', 'valid_for_year']].values.tolist()

        cursor.executemany(query, data)
```

With this you will be able to load your data to snowflake in the main script as the following example:

```py
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
    list_dir = os.listdir("data")  # this will get all the files and directories

    csv_files = filter(lambda item: item.endswith(".csv"),
                       list_dir)  # Making sure that we are just using the correct file format

    for current_file in csv_files:
        df = pd.read_csv(f'./data/{current_file}')
        _, year = current_file.split("_")
        year = year.replace(".csv", "")
        df["valid_for_year"] = year
        upload_to_snowflake(connection, df, "products")
```

## Conclusion

In this lesson we created a Change Data Capture (CDC) that keeps the data from description, price and stock. this, just by using the "valid_for_year". but if the name of the product changes we wouldn't be able to know or track it.

## Still curious

* So what is CDC?

  In simple terms, *CDC means to track the changes done to a source data in real time or near real time.* \
  In this practice we use backups, however real scenarios does not use backups as they are menat to be  real time or near real time, the most common way to do it is by using polling, logs or triggers.

* Real case study:

  Imagine you work at a highway goverment tracking, they need you to register and provide analytic data for the accidents occurring in some section of the road, currently you cannot modify the structure of the tables, but you can log in the triggers as much as needed.

  A solution would be to implement logs, that then will be collected tracking the information about type of accident, section of the road (km), insurance cost... and dump it into another database or datawarehouse to perform analysis.

* What other things can you do with CDC?

  Replication, Data Integration, Disaster Recovery, Data Migration, Audit and compliance...

* The things you need to have in mind when setting up a CDC are:
  * Change Identification: What changes do I need to track?
  * Granularity: How deep into the changes I need to go? (column, row, table...)
  * Real-time or Batch: How quick do I need the changes (schedule based or real time)
  * Capture Methods:
    * Log-Based CDC
    * Trigger-Based CDC
    * Polling-Based CDC
  * Timestamps or Sequence Numbers: How do I need to identify the order of changes?
  * Change Propagation: Once I got the changes, how do I want to deliver those changes to other systems? (Reports, other DBs, apps...)

* Check the following articles for more information:
  * Article: [What is CDC][what_si_cdc]
  * Article: [CDC with SQL Server][cdc_sql_server]

## Links

* [pyenv setup][py_env]
* [Pre Setup][pre_setup]

* [What is CDC][what_si_cdc]
* [CDC with SQL Server][cdc_sql_server]

[data_folder]: ./data

[pre_setup]: pre-setup%20README.md
[py_env]: ../session_4_Python_DE/PRE-SETUP%20README.md#Python%20Virtual%20Environment

[what_si_cdc]: https://www.redhat.com/en/topics/integration/what-is-change-data-capture
[cdc_sql_server]: https://learn.microsoft.com/en-us/sql/relational-databases/track-changes/about-change-data-capture-sql-server?view=sql-server-ver16
