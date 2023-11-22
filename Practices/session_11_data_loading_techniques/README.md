# Data Loading Techniques

In this practice we will get an approach to the most common loading techniques

## Prerequisites

* Follow the [pre-setup guideline][pre_setup]

## What You Will Learn

Loading techniques:

* `Truncate and reload`/`Full load`
* `Upsert`/`Delta` (Delta load)
* `Append`

Additional concepts for data structures

* External tables

## Before start

Let's review the concepts we will be applying during the practice

### External tables

Sometimes online storage like AWS, Azure or GCP is cheaper than Datawarehouse storage such as Snowflake, but most of the datawarehouses allow you to connect external tables

>External tables are tables where the declaration and storage are splitted, the declaration (schema) will be stored in the datawarehouse while the storage will occur on a different location (usually cloud)

Saving costs is one of the main purpouses for and external table, but is not the only one, also a big advantage is to be able to handle even more data than a traditional table, external tables behave very similar to an HDFS implementation

### Loading Techniques

* `Truncate and reload` \
  The `table is deleted` (not dropped) `then reloaded` with fresh data.
  >Useful when data is small or entire table need a refresh, can be time consuming and does not keep history

* `Incremental / Delta / Upsert` \
  The records since the last load are `updated`.
  >Useful with large amount of base data is having a small set of changes.

* `Append` \
  The records are versioned, updates are inserted as `new rows`.
  >This is very useful where the data is changing constantly and history is required to be maintained

## Practice

Practice the Truncate & reload, Delta & append based on the previous practice

### Requirements

Taking as base the database from the previous practice:

* Process the files on [data folder][data_folder]
* Track the company name

>Asume previous data is not useful with the new tracking data available

### Step 0 - Previous lesson

* Snowflake \
  If you have the previous practice complete, you should still have the table with the data. \
  If you don't have the previous practice complete:

  * Create a new database named `FUNDAMENTALS_DB`
  * Execute `snowflake.sql` on snowflake; the schema name must be `FUNDAMENTALS_DB`

* Python \
  If you have the previous practice complete, you should have the file `cdc.py` ready, let's keep the session a part, in the `practice_files` you will find the file `cdc.py`, so you can continue where you left it, but we still need to re-run another virtual environment

  ```sh
  # Virtual environment
  python3 -m venv myenv
  source myenv/bin/activate

  # Install packages to venv
  pip install pandas snowflake-connector-python
  ```

  * Also don't forget to replace your snowflake credentials on the `cdc.py` file

### Step 1 - Database

* Add a field to track company name

  ```sql
  ALTER TABLE products ADD COLUMN company_name VARCHAR(500);
  ```

### Step 2 - Generic Columns

On cdc.py you will find the function `upload_to_snowflake`, however this functions is not ready to handle the new column.

* Remove query and data so it remains as shown
  * Also let's change the `data` parameter in `cursor.executemany`

  ```py
  def upload_to_snowflake(connection: SnowflakeConnection, data_frame, table_name):
  with connection.cursor() as cursor:
    
    cursor.executemany(query, data_frame.values.tolist())
  ```

* Remove the `id` column from the data_frame

  ```py
  del data_frame['id']
  ```

* Add the new generic column handler before the cursor

  ```py
  column_secrets = ['%s'] * len(data_frame.columns)
  column_preparated_str = ','.join(column_secrets)
  query = f"INSERT INTO {table_name} VALUES ({column_preparated_str})"
  ```

### Step 3 - Company Name

We are still not handling the new column in the code, let's rework the code to do it

* We already have some code to handle files inside a folder, let's pass that to a separate function

  ```py
  def insert_company_data():
    list_dir = os.listdir("practice_files")

    for file_name in list_dir:
      df = pandas.read_csv(f'./practice_files/{file_name}')

      _, year = file_name.split("_")
      year = year.replace(".csv", "")
      df["valid_for_year"] = year

      upload_to_snowflake(connection, df, "products")
  ```

* Receive the company name parameter

  ```py
  # company_name should match a folder inside practice_files
  def insert_company_data(company_name):
  ```

* Handle the file list & file read

  ```py
  list_dir = os.listdir(f"data/{company_name}")

  for file_name in list_dir:
    df = pandas.read_csv(f'./data/{company_name}/{file_name}')
  ```

* Handle the new column

  ```py
  df["company_name"] = company
  ```

* Inside the snowflake connect, call the new function
  > Let's start with the `Company A` and see if its works

  ```py
  with connect(
    ...
  ) as connection:
    for company in ['Company A']:
      insert_company_data(company)
  ```

### Step 4 - Truncate

If you execute the script it will fail, because we changed the table structure, since the previous data is not valid anymore, we can apply a `Truncate & Reload`

* Go to snowflake an perform a truncate

  ```sql
  TRUNCATE TABLE products;
  ```

Run the code and verify the results on Snowflake

### Step 5 - Delta

* Add the Company B to the array of companies then run the code again and verify the results

  ```py
  with connect(
    ...
  ) as connection:
    for company in ['Company A', 'Company B']:
      insert_company_data(company)
  ```

### Step 6 - Append

* Add versioning to the table

  ```sql
  ALTER TABLE products ADD COLUMN inserted_at DATETIME;
  ```

* Normalize all previous data

  ```sql
  UPDATE products SET inserted_at = '2020-01-01';
  ```

* Add the new column

  ```py
  # Required import
  import datetime

  ...

  now = datetime.datetime.now()
  df["inserted_at"] = now.strftime('%Y-%m-%dT%H:%M:%S')
  ```

* Check the results in snowflake

>In a real worl scenario the `inserted_at` column can be a different value, even the time when the csv was received, or just an integer,

## Conclusion

In this practice, we explored various data loading techniques concepts and their implications in the context of managing and updating data in a database.

* On Step 4 we `Truncate` and `Reload` with the new data
* On Step 5 there was no need to Truncate again, so instead we applied a `Delta` Load
* On Step 6 We add a versioning on the field, so the next insert would be a `Append` type

## Homework (Optional)

* Write a dynamic query to select all products filtering only the latest version of each row using the column inserted_at
  * The query should work even after another batch of inserts (Don't use hardcoded values on the WHERE clause)

* Investigate:
  * Why we don't use `Append` as a commong practice in OLTP/OLAP databases?
  * Why we didn't parse the value from string to datetime when inserting from dataframe to snowflake?

* Change the script so we don't use an array

  ```py
  for company in ['Company A', 'Company B']:
  ```

  but instead detect all the companies in the `data` folder

## Stil curious

As you may imagine Truncate and reload is not the most used technique in general, this is because now that you've spent possibly hours and money processing your information you don't want to simply throw away that information. However there is still some usage for this data loading technique:

* Daily Data Refresh \
  In many business intelligence and reporting systems, data needs to be updated daily to provide the latest insights. The "Truncate and Reload" approach is used to clear out the previous day's data and load the most recent data from source systems.
* Historical Data Updates \
  When historical data needs to be corrected or updated, the "Truncate and Reload" approach is used. Historical data is removed from the table and replaced with corrected or updated data.
* Testing and Development \
  During the development and testing of data pipelines and ETL processes, it's common to use this technique to ensure a clean slate for each iteration of testing. It helps avoid data contamination from previous tests.
* Data Versioning \
  Some applications maintain different versions of data. When a new version is released, the previous version is truncated, and the new version is loaded into the system.
* Data Archiving \
  In cases where data needs to be archived periodically, the "Truncate and Reload" technique can be used to create archive tables. The existing data is truncated from the main table and loaded into an archive table for long-term storage.
* Table Partitioning \
  Some databases use partitioning to optimize data management. In partitioning strategies, older partitions are truncated and replaced with new data to keep the dataset manageable and efficient.
* Data Migration \
  When migrating data from one system to another or from one database to another, the "Truncate and Reload" method is used to ensure that the target system starts with a clean slate before the migration.
* Data Cleansing \
  In data cleansing processes, erroneous or duplicate data is removed from the table, and clean, corrected data is loaded back into the table.
* Periodic Data Updates \
  Certain applications require periodic data updates, such as financial systems that update stock prices every minute. Truncate and reload are used to ensure that the latest data is available.
* Snapshot Data \
  Some systems maintain snapshot data at regular intervals for historical analysis. The "Truncate and Reload" technique is used to replace the existing snapshot with the latest one.

Now on the other side, most of the time you will be using the other 2 techniques

Want to learn more about them:

* Article: [Why We Don’t Truncate Dimensions and Facts During a Data Load][truncate_facts]
* Article: [Incremental Data Load vs Full Load ETL][incremental_vs_full]

## Links

### Used during this session

* [Pre Setup][pre_setup]

* [Why We Don’t Truncate Dimensions and Facts During a Data Load][truncate_facts]
* [Incremental Data Load vs Full Load ETL][incremental_vs_full]

### Session reinforment and homework help

* Documentation: [Using Pandas DataFrames with the Python Connector][snowflake_pandas]
* Documentation: [Snowlflake: Data Types][snowflake_datatypes]

[data_folder]: ./practice_files/data/

[pre_setup]: pre-setup%20README.md

[truncate_facts]: https://datasavvy.me/2019/07/25/why-we-dont-truncate-dimensions-and-facts-during-a-data-load/
[incremental_vs_full]: https://hevodata.com/learn/incremental-data-load-vs-full-load/

[snowflake_pandas]: https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-pandas
[snowflake_datatypes]: https://docs.snowflake.com/en/sql-reference/data-types
