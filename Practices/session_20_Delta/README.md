# Practice: Lakehouse architecture with Iceberg and PySpark

In this practice you will learn how to use Iceberg and PySpark to create a lakehouse architecture.

## What you will learn

* Use MinIO as a local replacement for S3
* Use Iceberg to interface with MinIO
* Iceberg's S3 representation of data
* Issue DDL and DML commands with SparkSQL
* Iceberg's schema evolution capabilities
* Iceberg's time travel capabilities

## Pre-requisites

* Install Docker
* Install Docker Compose

## Before start

* What is Icerberg?

  >Iceberg is a high-performance format for huge analytic tables. Iceberg brings the reliability and simplicity of SQL tables to big data, while making it possible for engines like Spark, Trino, Flink, Presto, Hive and Impala to safely work with the same tables, at the same time.

  [Official documentation][iceberg]

* What is MinIO?

  >MinIO is a high-performance, S3 compatible object store. It is built for large scale AI/ML, data lake and database workloads. It is software-defined and runs on any cloud or on-premises infrastructure. MinIO is dual-licensed under open source GNU AGPL v3 and a commercial enterprise license.

  [Official documentation][minio]

* What is PySpark?

  >PySpark is the Python API for Apache Spark. It enables you to perform real-time, large-scale data processing in a distributed environment using Python. It also provides a PySpark shell for interactively analyzing your data.

  [Official documentation][pyspark]

## Practice

Use the data stored in `/home/iceberg/data` directory from the `spark-iceberg` image to:

* Create Icerberg catalog
  * Verify the count after linkin the data
* Do the following DDL operations
  * Rename `fare_amount` to `fare`
  * Rename `trip_distance` to `distance`
  * Add a float column `fare_per_distance_unit` immediately after `distance`.
    * Verify your columns with a SELECT
* Perform a row-level delete for all rows that have a `fare_per_distance_unit` greater than 4 or a `distance` greater than 2
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

### Create a table

We will use the New York City Taxi and Limousine Commision Trip Record Data that's available on the AWS Open Data Registry.

This contains data of trips taken by taxis and for-hire vehicles in New York City. We'll save this into an iceberg table called taxis. The data is already stored in the `/home/iceberg/data` directory in the `spark-iceberg` image.

Run the following command to create a table called `nyc.taxis` in the Iceberg catalog.

```py
df = spark.read.parquet("/home/iceberg/data/yellow_tripdata_2021-04.parquet")
df.write.saveAsTable("nyc.taxis")
```

Now run the following command to get a description of the table.

```py
spark.sql("DESCRIBE EXTENDED nyc.taxis").show(n=100, truncate=False)
```

Now run the following command to get the count of records in the table.

```py
spark.sql("SELECT COUNT(*) FROM nyc.taxis").show()
```

### Schema evolution

We can perform a wide range of DDL operations on Iceberg tables. Please refer to [Iceberg's documentation](https://iceberg.apache.org/docs/latest/spark-ddl/) for more information.

In this example, we'll rename `fare_amount` to `fare` and `trip_distance` to `distance`. We'll also add a float column `fare_per_distance_unit` immediately after `distance`.

```py
spark.sql("ALTER TABLE nyc.taxis RENAME COLUMN fare_amount TO fare")
spark.sql("ALTER TABLE nyc.taxis RENAME COLUMN trip_distance TO distance")
```

Now let's make a comment on the `distance` column.

```py
spark.sql("ALTER TABLE nyc.taxis ALTER COLUMN distance COMMENT 'The elapsed trip distance in miles reported by the taximeter.'")
```

We can perform safe data type conversions using the following command.

```py
spark.sql("ALTER TABLE nyc.taxis ALTER COLUMN distance TYPE double;")
spark.sql("ALTER TABLE nyc.taxis ALTER COLUMN distance AFTER fare;")
```

Now let's create a new column called `fare_per_distance_unit`.

```py
spark.sql("ALTER TABLE nyc.taxis ADD COLUMN fare_per_distance_unit float AFTER distance")
```

Let's update the new `fare_per_distance_unit` to equal `fare` divided by `distance`.

```py
spark.sql("UPDATE nyc.taxis SET fare_per_distance_unit = fare/distance")
```

Now query the table to see the new column.

```py
spark.sql("SELECT VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, fare, distance, fare_per_distance_unit FROM nyc.taxis").show()
```

### Expressive SQL for Row Level Changes

With Iceberg tables, `DELETE` queries can be used to perform row-level deletes. This is as simple as providing the table name and a `WHERE` predicate. If the filter matches an entire partition of the table, Iceberg will intelligently perform a metadata-only operation where it simply deletes the metadata for that partition.

Let's perform a row-level delete for all rows that have a `fare_per_distance_unit` greater than 4 or a `distance` greater than 2. This should leave us with relatively short trips that have a relatively high fare per distance traveled.

```py
spark.sql("DELETE FROM nyc.taxis WHERE fare_per_distance_unit > 4.0 OR distance > 2.0")
```

There are some fares that have a `null` for `fare_per_distance_unit` due to the distance being `0`. Let's remove those as well.

```py
spark.sql("DELETE FROM nyc.taxis WHERE fare_per_distance_unit IS NULL")
```

```py
spark.sql("SELECT VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, fare, distance, fare_per_distance_unit FROM nyc.taxis").show()
```

Finally, let's count the number of rows in the table.

```py
spark.sql("SELECT COUNT(*) FROM nyc.taxis").show()
```

### Partitioning

A table’s partitioning can be updated in place and applied only to newly written data. Query plans are then split, using the old partition scheme for data written before the partition scheme was changed, and using the new partition scheme for data written after. People querying the table don’t even have to be aware of this split. Simple predicates in WHERE clauses are automatically converted to partition filters that prune out files with no matches. This is what’s referred to in Iceberg as *Hidden Partitioning*.

```py
spark.sql("ALTER TABLE nyc.taxis ADD PARTITION FIELD VendorID")
```

### Metadata tables

Iceberg tables contain very rich metadata that can be easily queried. For example, you can retrieve the manifest list for any snapshot, simply by querying the table's `snapshots` table.

```py
spark.sql("SELECT snapshot_id, manifest_list FROM nyc.taxis.snapshots").show()
```

The `files` table contains loads of information on data files, including column level statistics such as null counts, lower bounds, and upper bounds.

```py
spark.sql("SELECT file_path, file_format, record_count, null_value_counts, lower_bounds, upper_bounds FROM nyc.taxis.files").show(n=100, truncate=False)
```

### Time travel

The history table lists all snapshots and which parent snapshot they derive from. The `is_current_ancestor` flag let's you know if a snapshot is part of the linear history of the current snapshot of the table.

```py
spark.sql("SELECT * FROM nyc.taxis.history").show()
```

You can time-travel by altering the `current-snapshot-id` property of the table to reference any snapshot in the table's history. Let's revert the table to its original state by traveling to the very first snapshot ID.

Let's retrieve the first snapshot ID.

```py
df = spark.sql("SELECT * FROM nyc.taxis.history")
original_snapshot = df.head().snapshot_id
print(original_snapshot)
```

Now let's travel to the first snapshot. Here, `demo` is the name of the default catalog, as specified in the `spark/spark-defaults.conf` file. If you're using a different catalog, you'll need to change this to the appropriate catalog name.

For more details on Spark procedures, please refer to the [Iceberg's documentation](https://iceberg.apache.org/docs/latest/spark-procedures/).

```py
spark.sql(f"CALL demo.system.rollback_to_snapshot('nyc.taxis', {original_snapshot})")
```

```py
spark.sql("SELECT VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, fare, distance, fare_per_distance_unit FROM nyc.taxis").show()
```

Another look at the history table shows that the original state of the table has been added as a new entry
with the original snapshot ID.

```py
spark.sql("SELECT * FROM nyc.taxis.history").show()
```

```py
spark.sql("SELECT COUNT(*) as cnt FROM nyc.taxis").show()
```

### The Iceberg data representation

Iceberg tables are stored in a directory hierarchy. The root directory contains a metadata directory and a data directory. The metadata directory contains the table metadata files, while the data directory contains the data files.

Access the MinIO web console at <http://localhost:9000> and navigate to the `warehouse` bucket. Click in the `wh` and access the `nyc` and `taxis` directories. You should see the `data` and `metadata` directories.

As you can see, most of the metadata is stored in JSON files. You can download a couple of these to see the structure of the metadata.

### Cleanup

To stop the Spark cluster, run the following command:

```bash
docker-compose down
```

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

* [Icerberg][iceberg]
* [MinIO][minio]
* [PySpark][pyspark]
* Article: [5 Compelling Reasons to Choose Apache Iceberg][choose_iceberg]
* Documentation: [AT|BEFORE Clause][snowflake_timetravel]
* Practice: [Getting Started with Time Travel][snowflake_timetravel_practice]
* [Amazon S3 vs. Google Cloud Storage vs. IBM Cloud Object Storage vs. MinIO][minio_alternatives]

[iceberg]: https://iceberg.apache.org/
[minio]: https://min.io/
[pyspark]: https://spark.apache.org/docs/latest/api/python/index.html

[choose_iceberg]: https://www.snowflake.com/blog/5-reasons-apache-iceberg/
[snowflake_timetravel]: https://docs.snowflake.com/en/sql-reference/constructs/at-before
[snowflake_timetravel_practice]: https://quickstarts.snowflake.com/guide/getting_started_with_time_travel/index.html?index=..%2F..index#0
[minio_alternatives]: https://slashdot.org/software/comparison/Amazon-S3-vs-Google-Cloud-Storage-vs-IBM-Cloud-Object-Storage-vs-Minio/
