# Lakehouse architecture with Iceberg and PySpark

In this practice you will learn how to use Iceberg and PySpark to create a lakehouse architecture.

## Pre-requisites

* Follow the [pre-setup guideline][pre-setup]

## Before start

Let's review some tecnologies we used during the pre-setup:

* `Icerberg` \
  Iceberg is a high-performance format for huge analytic tables. Iceberg brings the reliability and simplicity of SQL tables to big data, while making it possible for engines like Spark, Trino, Flink, Presto, Hive and Impala to safely work with the same tables, at the same time.

  [Official documentation][iceberg]

* `MinIO` \
  MinIO is a high-performance, S3 compatible object store. It is built for large scale AI/ML, data lake and database workloads. It is software-defined and runs on any cloud or on-premises infrastructure. MinIO is dual-licensed under open source GNU AGPL v3 and a commercial enterprise license.

  [Official documentation][minio]

* `PySpark`
  PySpark is the Python API for Apache Spark. It enables you to perform real-time, large-scale data processing in a distributed environment using Python. It also provides a PySpark shell for interactively analyzing your data.

  [Official documentation][pyspark]

## What you will learn

* Use MinIO as a local replacement for S3
* Use Iceberg to interface with MinIO
* Iceberg's S3 representation of data
* Issue DDL and DML commands with SparkSQL
* Iceberg's schema evolution capabilities
* Iceberg's time travel capabilities

## Practice

Explore the infrastructure of MinIO, Iceberg with PySpark

>Use the New York City Taxi and Limousine Commision Trip Record Data that's available on the AWS Open Data Registry. \
>The data is already stored in the `/home/iceberg/data` directory in the `spark-iceberg` image.

### Requirements

Use the data stored in `/home/iceberg/data` directory from the `spark-iceberg` image to:

* Create Icerberg catalog (`nyc.taxis`)
  * Use one of the pre-existent parquet files as table structure
  * Verify the count after linkin the data
* Do the following DDL operations
  * Rename `fare_amount` to `fare`
  * Rename `trip_distance` to `distance`
  * Add a comment for documentation on `distance` column
  * Change `fare` type to double and move it after `distance`
  * Add a float column `fare_per_distance_unit` immediately after `distance` \
    *Set value of new column as `fare/distance`*
    * Verify your columns with a SELECT
* Delete rows where `fare_per_distance_unit` greater than 4 or a `distance` greater than 2
  * Verify the count and compare with full catalog (first query after loading the catalog)
* Partition the table by `VendorID` field
* Query metadata tables
  * `snapshots`
  * `files`
* Time travel
  * Get current snapshot id
  * Query all elements from the table
  * Rollback to a previous snapshot
  * Query all elements from the table

### Step 0 - Explore infrastructure

`MinIO` \
Login to webUI for MinIO on <http://localhost:9000> use the following credentials `admin`/`password` \
This will be your S3 replacement

`PySpark` shell \
As with previous practices we will be executing python instructions from spark image, in order to do this start the shell attached to docker:

```sh
docker exec -it spark-iceberg pyspark
```

### Step 1 - Iceberg Table

* Create `nyc.taxis` on Iceberg Catalog

  ```py
  df = spark.read.parquet("/home/iceberg/data/yellow_tripdata_2021-04.parquet")
  df.write.saveAsTable("nyc.taxis")
  ```

* Verify table structure

  ```py
  spark.sql("DESCRIBE EXTENDED nyc.taxis").show(n=100, truncate=False)
  ```

* Verify data exists on table

  ```py
  spark.sql("SELECT COUNT(*) FROM nyc.taxis").show()
  ```

### Step 2 - Schema evolution

* Rename `fare_amount` to `fare` and `trip_distance` to `distance`

  ```py
  spark.sql("ALTER TABLE nyc.taxis RENAME COLUMN fare_amount TO fare")
  spark.sql("ALTER TABLE nyc.taxis RENAME COLUMN trip_distance TO distance")
  ```

* Make a comment on the `distance` column.

  ```py
  spark.sql("ALTER TABLE nyc.taxis ALTER COLUMN distance COMMENT 'The elapsed trip distance in miles reported by the taximeter.'")
  ```

* Data type conversion

  ```py
  spark.sql("ALTER TABLE nyc.taxis ALTER COLUMN distance TYPE double;")
  spark.sql("ALTER TABLE nyc.taxis ALTER COLUMN distance AFTER fare;")
  ```

* Create column `fare_per_distance_unit`.

  ```py
  spark.sql("ALTER TABLE nyc.taxis ADD COLUMN fare_per_distance_unit float AFTER distance")
  ```

* Set value for new column

  ```py
  spark.sql("UPDATE nyc.taxis SET fare_per_distance_unit = fare/distance")
  ```

* Query to see the new column

  ```py
  spark.sql("SELECT VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, fare, distance, fare_per_distance_unit FROM nyc.taxis").show()
  ```

### Step 3 - Row level changes

* Delete where `fare_per_distance_unit` greater than 4 or a `distance` greater than 2

  ```py
  spark.sql("DELETE FROM nyc.taxis WHERE fare_per_distance_unit > 4.0 OR distance > 2.0")
  ```

* Include Coalesce values into the delete

  ```py
  spark.sql("DELETE FROM nyc.taxis WHERE fare_per_distance_unit > 4.0 OR distance > 2.0 OR fare_per_distance_unit IS NULL")
  ```

* Verify results

  ```py
  spark.sql("SELECT VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, fare, distance, fare_per_distance_unit FROM nyc.taxis").show()
  ```

* Get the table count

  ```py
  spark.sql("SELECT COUNT(*) FROM nyc.taxis").show()
  ```

### Step 4 - Partitioning

* Partition by `VendorID`

  ```py
  spark.sql("ALTER TABLE nyc.taxis ADD PARTITION FIELD VendorID")
  ```

### Step 5 - Query metadata

Iceberg contain metadata tables, some examples being `snapshots` or `files`, let's perform some querys on these

* Query taxis `snapshots`

  ```py
  spark.sql("SELECT snapshot_id, manifest_list FROM nyc.taxis.snapshots").show()
  ```

* Query `files`

  ```py
  spark.sql("SELECT file_path, file_format, record_count, null_value_counts, lower_bounds, upper_bounds FROM nyc.taxis.files").show(n=100, truncate=False)
  ```

### Step 6 - Time travel

Another useful metadata table is `history`, which allow you to view different versions of your table

* Query `history`

  ```py
  spark.sql("SELECT * FROM nyc.taxis.history").show()
  ```

* Get current snapshot id

  ```py
  df = spark.sql("SELECT * FROM nyc.taxis.history")
  original_snapshot = df.head().snapshot_id
  print(original_snapshot)
  ```

* Query all elements from the table

  ```py
  spark.sql("SELECT VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, fare, distance, fare_per_distance_unit FROM nyc.taxis").show()
  ```

* Rollback to a previous snapshot

  ```py
  spark.sql(f"CALL demo.system.rollback_to_snapshot('nyc.taxis', {original_snapshot})")
  ```

* Query all elements from the table

  ```py
  spark.sql("SELECT VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, fare, distance, fare_per_distance_unit FROM nyc.taxis").show()
  ```

Another look at the history table shows that the original state of the table has been added as a new entry
with the original snapshot ID.

```py
spark.sql("SELECT * FROM nyc.taxis.history").show()
spark.sql("SELECT COUNT(*) as cnt FROM nyc.taxis").show()
```

### The Iceberg data representation

Iceberg tables are stored in a directory hierarchy. The root directory contains a metadata directory and a data directory. The metadata directory contains the table metadata files, while the data directory contains the data files.

Access the MinIO web console at <http://localhost:9000> and navigate to the `warehouse` bucket. Click in the `wh` and access the `nyc` and `taxis` directories. You should see the `data` and `metadata` directories.

As you can see, most of the metadata is stored in JSON files. You can download a couple of these to see the structure of the metadata.

## Still curious

* Apache Iceberg is one of many solutions for DataLake, in the article below you can go deep to when to use it, according to Snowflake

  Article: [5 Compelling Reasons to Choose Apache Iceberg][choose_iceberg]

* Did you know the "time travel" feature is not exclusive to Iceberg?

  Some other systems can offer their version too, take snowflake as example:

  * Documentation: [AT|BEFORE Clause][snowflake_timetravel]
  * Practice: [Getting Started with Time Travel][snowflake_timetravel_practice]

* MinIO is also another tool that has some alternatives, in the comparison below you can check how it compares against similar services:
  * [Amazon S3 vs. Google Cloud Storage vs. IBM Cloud Object Storage vs. MinIO][minio_alternatives]

## Links

### Used during this session

* [Pre-Setup][pre-setup]
* [Icerberg][iceberg]
* [MinIO][minio]
* [PySpark][pyspark]

### Session reinforment and homework help

* [Iceberg's DDL documentation][iceberg_ddl]
* Article: [5 Compelling Reasons to Choose Apache Iceberg][choose_iceberg]
* Documentation: [AT|BEFORE Clause][snowflake_timetravel]
* Practice: [Getting Started with Time Travel][snowflake_timetravel_practice]
* [Amazon S3 vs. Google Cloud Storage vs. IBM Cloud Object Storage vs. MinIO][minio_alternatives]

[pre-setup]: ./pre-setup.md

[iceberg]: https://iceberg.apache.org/
[minio]: https://min.io/
[pyspark]: https://spark.apache.org/docs/latest/api/python/index.html

[iceberg_ddl]: https://iceberg.apache.org/docs/latest/spark-ddl/
[choose_iceberg]: https://www.snowflake.com/blog/5-reasons-apache-iceberg/
[snowflake_timetravel]: https://docs.snowflake.com/en/sql-reference/constructs/at-before
[snowflake_timetravel_practice]: https://quickstarts.snowflake.com/guide/getting_started_with_time_travel/index.html?index=..%2F..index#0
[minio_alternatives]: https://slashdot.org/software/comparison/Amazon-S3-vs-Google-Cloud-Storage-vs-IBM-Cloud-Object-Storage-vs-Minio/
