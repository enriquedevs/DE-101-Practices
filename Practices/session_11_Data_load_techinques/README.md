# Data Load Techniques

This practice is intended to teach you which are the types of data load.
In this practice, you will learn what are the implications for this three load techniques

- Upsert/Delta load/Append
- Truncate and reload/Full load
- External tables


## External tables

while this is not a Load technique like the other two, this is a very helpful tool to reduce
costs, because you will store your data into an S3 bucket instead of a normal table, and is also
useful for ELT processes.


# Practice

According to the last pipeline `session_10_Fundamentals` we need to do a few changes to the table.

First of all, this time we have information for another company, and we don't want the data to be mixed
or wrong, so we need to add another column to the table and the python script.

## Step 1

#### Table

```snowflake
    ALTER TABLE FUNDAMENTALS_DB.PRODUCTS ADD COLUMN company_name VARCHAR(500);
```

## Step 2

#### Script

Once that we have the table updated, we need to update some data in our script.

let's see where.

```python
def upload_to_snowflake(connection: SnowflakeConnection, data_frame, table_name):
    with connection.cursor() as cursor:
        query = f"INSERT INTO {table_name} (name, description, price, stock, valid_for_year) VALUES (%s, %s, %s, %s, %s)"
        data = data_frame[['name', 'description', 'price', 'stock', 'valid_for_year']].values.tolist()

        cursor.executemany(query, data)
```

in this section of the script, the problem is that the columns are explicitly placed, let''s change it'

```python
import pandas as pd


def upload_to_snowflake(connection: SnowflakeConnection, data_frame: pd.DataFrame, table_name):
    data_frame.drop("id")
    
    with connection.cursor() as cursor:
        column_secrets = ['?'] * len(data_frame.columns)
        column_preparated_str = ','.join(column_secrets)
        query = f"INSERT INTO {table_name} VALUES ({column_preparated_str})"
        cursor.executemany(query, data_frame.values.tolist())
```

## Step 3

now we can load the whole data without worrying about the new columns that we added.
The only problem would be that we need to differentiate the new data for Company A.

so we just need to add after

```python
df["valid_for_year"] = year
```

the following line
```python
df["company_name"] = "Company A"
```

## Step 4

The only problem is that due to the structure change, we need to truncate the table.

```snowflake
TRUNCATE TABLE FUNDAMENTALS_DB.PRODUCTS;
```

and then we can run the python script that uploads the data.

## Step 5

Use the `generator.py` script (remember to install pandas) to create the whole data for 
company B (this is done this way so the repository is not bigger than it should) and load it.

Now we need to add the company B data, just adjust the origin of the data to the new files and change
the company_name to "Company B".

# Conclusion

We used the Delta load and truncate and reload.
When we tried to load data for the new table structure, we truncated the table data, and we loaded again everything.
And then the Delta load by just adding te data for company B without removing company A's data.