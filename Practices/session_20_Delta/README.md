# Practice: Lakehouse architecture with Iceberg and PySpark

In this practice you will learn how to use Iceberg and PySpark to create a lakehouse architecture.

## What you will learn

- Use MinIO as a local replacement for S3
- Use Iceberg to interface with MinIO
- Iceberg's S3 representation of data
- Issue DDL and DML commands with SparkSQL
- Iceberg's schema evolution capabilities
- Iceberg's time travel capabilities

## Pre-requisites

- Install Docker
- Install Docker Compose

## Setup

### Docker Compose

First create a `docker-compose.yml` file with the following contents. We will add one service at a time.

```yaml
version: "3"

services:
```

#### MinIO

First, add the MinIO service to the `docker-compose.yml` file. MinIO is a High Performance Object Storage released under GNU Affero General Public License v3.0. It is API compatible with Amazon S3 cloud storage service.

```yaml
  minio:
    image: minio/minio
    container_name: minio
    environment:
      - MINIO_ROOT_USER=admin
      - MINIO_ROOT_PASSWORD=password
    ports:
      - 9001:9001
      - 9000:9000
    command: ["server", "/data", "--console-address", ":9001"]
```

#### MinIO Client

Next, add the MinIO Client service to the `docker-compose.yml` file. The MinIO Client is a command line tool for interacting with the MinIO server. This `entrypoint` command will create a bucket called `minio` and add a directory called `warehouse` to the bucket.

```yaml
  mc:
    depends_on:
      - minio
    image: minio/mc
    container_name: mc
    environment:
      - AWS_ACCESS_KEY_ID=admin
      - AWS_SECRET_ACCESS_KEY=password
      - AWS_REGION=us-east-1
    entrypoint: >
      /bin/sh -c "
      until (/usr/bin/mc config host add minio http://minio:9000 admin password) do echo '...waiting...' && sleep 1; done;
      /usr/bin/mc rm -r --force minio/warehouse;
      /usr/bin/mc mb minio/warehouse;
      /usr/bin/mc policy set public minio/warehouse;
      exit 0;
      "
```

#### Iceberg

Now, add the Iceberg REST catalog service to the `docker-compose.yml` file. This service simply exposes a REST interface for Spark to connect to. Spark doesn’t need to be concerned with connecting to the actual datastore which can be anything ranging from a Hive metastore to a MySQL database.

```yaml
  rest:
    image: tabulario/iceberg-rest:0.2.0
    ports:
      - 8181:8181
    environment:
      - AWS_ACCESS_KEY_ID=admin
      - AWS_SECRET_ACCESS_KEY=password
      - AWS_REGION=us-east-1
      - CATALOG_WAREHOUSE=s3a://warehouse/wh/
      - CATALOG_IO__IMPL=org.apache.iceberg.aws.s3.S3FileIO
      - CATALOG_S3_ENDPOINT=http://minio:9000
```

#### Spark+Iceberg

Finally, add the `spark-iceberg` service to the `docker-compose.yml` file. This service is described in the `Dockerfile` inside the `spark` directory in this repository. Please refer to the specification if you want to know more about the image.

```yaml
  spark-iceberg:
    build:
      context: ./spark
      dockerfile: Dockerfile
    container_name: spark-iceberg
    depends_on:
      - rest
      - minio
    environment:
      - AWS_ACCESS_KEY_ID=admin
      - AWS_SECRET_ACCESS_KEY=password
      - AWS_REGION=us-east-1
    ports:
      - 8888:8888
      - 8080:8080
      - 10000:10000
      - 10001:10001
    links:
      - rest:rest
      - minio:minio
```

### Build and start the environment

Start up the Icebeberg and PySpark environment by running the following.

```bash
docker-compose up --build
```

You can then access the MinIO UI at <http://localhost:9000>. The Username is `admin` and the password is `password`.

MinIO is a local replacement for S3. It is a simple object storage server that is compatible with the Amazon S3 API. It is used in this practice to simulate a cloud storage environment.

You also can access the PySpark REPL by running the following.

```bash
docker exec -it spark-iceberg pyspark
```

Run the following command to confirm that the `spark` session successfully started. We will use this session to interact with Iceberg.

```python
spark.sparkContext.getConf().getAll()
```

## The practice

### Create a table

We will use the New York City Taxi and Limousine Commision Trip Record Data that's available on the AWS Open Data Registry. This contains data of trips taken by taxis and for-hire vehicles in New York City. We'll save this into an iceberg table called taxis. The data is already stored in the `/home/iceberg/data` directory in the `spark-iceberg` image.

Run the following command to create a table called `nyc.taxis` in the Iceberg catalog.

```python
df = spark.read.parquet("/home/iceberg/data/yellow_tripdata_2021-04.parquet")
df.write.saveAsTable("nyc.taxis")
```

Now run the following command to get a description of the table.

```python
spark.sql("DESCRIBE EXTENDED nyc.taxis").show(n=100, truncate=False)
```

Now run the following command to get the count of records in the table.

```python
spark.sql("SELECT COUNT(*) FROM nyc.taxis").show()
```

### Schema evolution

We can perform a wide range of DDL operations on Iceberg tables. Please refer to [Iceberg's documentation](https://iceberg.apache.org/docs/latest/spark-ddl/) for more information.

In this example, we'll rename `fare_amount` to `fare` and `trip_distance` to `distance`. We'll also add a float column `fare_per_distance_unit` immediately after `distance`.

```python
spark.sql("ALTER TABLE nyc.taxis RENAME COLUMN fare_amount TO fare")
spark.sql("ALTER TABLE nyc.taxis RENAME COLUMN trip_distance TO distance")
```

Now let's make a comment on the `distance` column.

```python
spark.sql("ALTER TABLE nyc.taxis ALTER COLUMN distance COMMENT 'The elapsed trip distance in miles reported by the taximeter.'")
```

We can perform safe data type conversions using the following command.

```python
spark.sql("ALTER TABLE nyc.taxis ALTER COLUMN distance TYPE double;")
spark.sql("ALTER TABLE nyc.taxis ALTER COLUMN distance AFTER fare;")
```

Now let's create a new column called `fare_per_distance_unit`.

```python
spark.sql("ALTER TABLE nyc.taxis ADD COLUMN fare_per_distance_unit float AFTER distance")
```

Let's update the new `fare_per_distance_unit` to equal `fare` divided by `distance`.

```python
spark.sql("UPDATE nyc.taxis SET fare_per_distance_unit = fare/distance")
```

Now query the table to see the new column.

```python
spark.sql("SELECT VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, fare, distance, fare_per_distance_unitF ROM nyc.taxis").show()
```

### Expressive SQL for Row Level Changes

With Iceberg tables, `DELETE` queries can be used to perform row-level deletes. This is as simple as providing the table name and a `WHERE` predicate. If the filter matches an entire partition of the table, Iceberg will intelligently perform a metadata-only operation where it simply deletes the metadata for that partition.

Let's perform a row-level delete for all rows that have a `fare_per_distance_unit` greater than 4 or a `distance` greater than 2. This should leave us with relatively short trips that have a relatively high fare per distance traveled.

```python
spark.sql("DELETE FROM nyc.taxis WHERE fare_per_distance_unit > 4.0 OR distance > 2.0")
```

There are some fares that have a `null` for `fare_per_distance_unit` due to the distance being `0`. Let's remove those as well.

```python
spark.sql("DELETE FROM nyc.taxis WHERE fare_per_distance_unit IS NULL")
```

```python
spark.sql("SELECT VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, fare, distance, fare_per_distance_unitF ROM nyc.taxis").show()
```

Finally, let's count the number of rows in the table.

```python
spark.sql("SELECT COUNT(*) FROM nyc.taxis").show()
```

### Partitioning

A table’s partitioning can be updated in place and applied only to newly written data. Query plans are then split, using the old partition scheme for data written before the partition scheme was changed, and using the new partition scheme for data written after. People querying the table don’t even have to be aware of this split. Simple predicates in WHERE clauses are automatically converted to partition filters that prune out files with no matches. This is what’s referred to in Iceberg as *Hidden Partitioning*.

```python
spark.sql("ALTER TABLE nyc.taxis ADD PARTITION FIELD VendorID")
```

### Metadata tables

Iceberg tables contain very rich metadata that can be easily queried. For example, you can retrieve the manifest list for any snapshot, simply by querying the table's `snapshots` table.

```python
spark.sql("SELECT snapshot_id, manifest_list FROM nyc.taxis.snapshots").show()
```

The `files` table contains loads of information on data files, including column level statistics such as null counts, lower bounds, and upper bounds.

```python
spark.sql("SELECT file_path, file_format, record_count, null_value_counts, lower_bounds, upper_bounds FROM nyc.taxis.files").show(n=100, truncate=False)
```

### Time travel

The history table lists all snapshots and which parent snapshot they derive from. The `is_current_ancestor` flag let's you know if a snapshot is part of the linear history of the current snapshot of the table.

```python
spark.sql("SELECT * FROM nyc.taxis.history").show()
```

You can time-travel by altering the `current-snapshot-id` property of the table to reference any snapshot in the table's history. Let's revert the table to its original state by traveling to the very first snapshot ID.

Let's retrieve the first snapshot ID.

```python
df = spark.sql("SELECT * FROM nyc.taxis.history")
original_snapshot = df.head().snapshot_id
print(original_snapshot)
```

Now let's travel to the first snapshot. Here, `demo` is the name of the default catalog, as specified in the `spark/spark-defaults.conf` file. If you're using a different catalog, you'll need to change this to the appropriate catalog name.

For more details on Spark procedures, please refer to the [Iceberg's documentation](https://iceberg.apache.org/docs/latest/spark-procedures/).

```python
spark.sql(f"CALL demo.system.rollback_to_snapshot('nyc.taxis', {original_snapshot})")
```

```python
spark.sql("SELECT VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, fare, distance, fare_per_distance_unitF ROM nyc.taxis").show()
```

Another look at the history table shows that the original state of the table has been added as a new entry
with the original snapshot ID.

```python
spark.sql("SELECT * FROM nyc.taxis.history").show()
```

```python
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
