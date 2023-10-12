# Data Load Techniques

This practice is intended to teach you which are the types of data load.
In this practice, you will learn what are the implications for this three load techniques

* Upsert/Delta load/Append
* Truncate and reload/Full load
* External tables

## External tables

while this is not a Load technique like the other two, this is a very helpful tool to reduce
costs, because you will store your data into an S3 bucket instead of a normal table, and is also
useful for ELT processes.

## Loading Techniques

* **Truncate and reload**

    In this method, the entire table is deleted and then reloaded with fresh data. This method is useful when the data is small or the entire table needs to be refreshed. However, it can be time-consuming and can cause data loss if not done carefully.

* **Incremental/Delta/Upsert**

    In this method, only the changes made since the last data load are loaded into the table. This method is useful when the data is large and only a small amount of data has changed since the last load. This can reduce the amount of data that needs to be loaded and can save time. Depending on the specific implementation, this method may be referred to as incremental, delta, or upsert.

* **Append**:

    In this method, new data is added to the existing data in the table. This method is useful when the new data needs to be added to the existing data rather than replacing it. This method can be used for cases where the data is constantly being updated and needs to be refreshed regularly.

## Practice

According to the last pipeline `session_10_Fundamentals` we need to do a few changes to the table.

First of all, this time we have information for another company, and we don't want the data to be mixed
or wrong, so we need to add another column to the table and the python script.

### Step 1 - Table

```sql
    ALTER TABLE FUNDAMENTALS_DB.PRODUCTS ADD COLUMN company_name VARCHAR(500);
    OK
```

### Step 2 - Python Script

Once that we have the table updated, we need to update some data in our script.

```py
def upload_to_snowflake(connection: SnowflakeConnection, data_frame, table_name):
    with connection.cursor() as cursor:
        query = f"INSERT INTO {table_name} (name, description, price, stock, valid_for_year) VALUES (%s, %s, %s, %s, %s)"
        data = data_frame[['name', 'description', 'price', 'stock', 'valid_for_year']].values.tolist()

        cursor.executemany(query, data)
```

in this section of the script, the problem is that the columns are explicitly placed, let''s change it'

```py
import pandas as pd

def upload_to_snowflake(connection: SnowflakeConnection, data_frame: pd.DataFrame, table_name):
    data_frame = data_frame.drop("id", axis=1)
    
    with connection.cursor() as cursor:
        column_secrets = ['%s'] * len(data_frame.columns)
        column_preparated_str = ','.join(column_secrets)
        query = f"INSERT INTO {table_name} VALUES ({column_preparated_str})"
        cursor.executemany(query, data_frame.values.tolist())
        print('Data Frame inserted!')
```

### Step 3 - Add new columns

now we can load the whole data without worrying about the new columns that we added.
The only problem would be that we need to differentiate the new data for Company A.

so we just need to add after

```py
df["valid_for_year"] = year
```

the following line

```py
df["company_name"] = "Company A"
```

### Step 4 - Truncate

The only problem is that due to the structure change, we need to truncate the table:

```sql
TRUNCATE TABLE FUNDAMENTALS_DB.PRODUCTS;
```

Then we can run the python script that uploads the data.

### Step 5 - Load both companies

Let's use a generic function to load both company A and company B, it can be the following

```py
def insert_company_data(company):
    list_dir = os.listdir(company) 

    csv_files = filter(lambda item: item.endswith(".csv"),
                       list_dir)  # Making sure that we are just using the correct file format


    for current_file in csv_files:
        print(current_file)
        df = pd.read_csv(f'./{company}/{current_file}')
        _, year = current_file.split("_")
        year = year.replace(".csv", "")
        df["valid_for_year"] = year
        df["company_name"] = company
        print(df)
        upload_to_snowflake(connection, df, "products")
```

### Step 6 - Calling the new function

Now let's call this function inside the snowflake connect code as

```py
with connect(
    account="jmb####",
    user="my_user",
    password="yourpassword",
    database="fundamentals_db",
    warehouse="COMPUTE_WH",
    region="us-west-2"
) as connection:

    for company in ['Company A', 'Company B']:
        insert_company_data(company)
```

### Step 7 - Verify

After running the code, both companies data should be in the table

## Conclusion

In this practice, we explored various data loading techniques and their implications in the context of managing and updating data in a database. \ We covered three primary data loading techniques, Truncate and Reload, Incremental/Delta/Upsert, Append

Additionally, we introduced the concept of External Tables, a powerful tool that, while not a loading technique per se, offers cost-saving benefits.

We used the Delta load and truncate and reload:

* When we tried to load data for the new table structure, we truncated the table data, and we loaded again everything.
* The Delta when we load by just adding te data for company B without removing company A's data.

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

* [Why We Don’t Truncate Dimensions and Facts During a Data Load][truncate_facts]
* [Incremental Data Load vs Full Load ETL][incremental_vs_full]

[truncate_facts]: https://datasavvy.me/2019/07/25/why-we-dont-truncate-dimensions-and-facts-during-a-data-load/
[incremental_vs_full]: https://hevodata.com/learn/incremental-data-load-vs-full-load/
