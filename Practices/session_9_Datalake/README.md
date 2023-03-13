# Datalake

In this practice we will setup a datalake on HDFS and Hive environment.

![Docker-Python](documentation_images/data-lake.jpg)

### Prerequisites
* [Install docker](https://docs.docker.com/engine/install/) 

### What You Will Learn
- Datalake Concepts and Components
- Hive
- HDFS
- Implement a Datalake on HDFS and Hive

# Practice

You're working on a global e-commerce company, and the company recieves multiple CSV and JSON files every day about the products that has been sold.

The company wants to have the product information into a single source that can be consumed by other systems. To achieve that, the company wants you to design and implement a datalake for it.

![img](documentation_images/data-lake-2.jpeg)

### Requirements
* Create a Datalake for the product files of the e-commerce.

## Step 1

### Datalake

A datalake is a centralized repository that allows you to **store and manage large volumes of structured, semi-structured, and unstructured data**. In a datalake, data is stored in its raw form, without any transformation or pre-processing, so that it can be accessed and analyzed by different teams across the organization. Also the **data or files stored on the datalake, it can be given an schema so that way you can query the data of the files on regular SQL**.

![Docker-Python](documentation_images/data-lake-3.jpeg)

### Where can be implemented a Datalake?

There are several different forms in which a datalake can be implemented, depending on the technologies and tools that are used. Some of the most common implementations of datalakes include:

+ **HDFS with Hive**: As I mentioned earlier, HDFS and Hive are commonly used to implement datalakes. HDFS provides a distributed file system for storing large volumes of data, while Hive provides a SQL-like interface for querying and analyzing the data.
+ **S3 with Athena**: Amazon S3 is a cloud-based storage service that is commonly used to implement datalakes. Athena is a serverless query service that allows you to run SQL queries against data stored in S3. This combination provides a scalable and cost-effective solution for storing and querying large volumes of data.
+ **Azure Blob Storage with Azure Data Lake Analytics**: Microsoft Azure provides Blob Storage, which is a scalable and secure cloud storage solution that can be used to store large volumes of data. Azure Data Lake Analytics is a serverless analytics service that allows you to run big data analytics jobs against data stored in Blob Storage.
+ **Google Cloud Storage with BigQuery**: Google Cloud Storage is a scalable and secure cloud storage solution that can be used to implement a datalake. BigQuery is a fully-managed data warehouse service that allows you to run SQL queries against data stored in Cloud Storage.

![Docker-Python](documentation_images/data-lake-6.png)

### How to Implement a Data Lake on HDFS/Hive

To implement a datalake using HDFS and Hive, you would typically follow these steps:

1. **Ingest data into HDFS**: The first step is to ingest the data that you want to store into HDFS. This can be done using a variety of tools, including Apache Kafka, Apache Flume, and Apache NiFi. The data can be stored in its raw form, without any transformation or pre-processing.
2. **Define a schema**: Once the data is stored in HDFS, you can define a schema for it using Hive. This involves creating a table that defines the structure of the data, including the column names, data types, and any other metadata that is required.
3. **Query the data**: Once the schema is defined, you can query the data using HiveQL. Hive will automatically map the queries to the data stored in HDFS, and it will distribute the queries across the nodes in the Hadoop cluster to perform the analysis at scale.
4. **Iterate and refine**: As you work with the data, you may discover that the schema needs to be refined or updated to better support your analysis. Hive allows you to easily modify the schema as needed, without having to manually modify the data stored in HDFS.

![Docker-Python](documentation_images/data-lake-8.png)

### How files can be stored on a Datalake's Filesystem

If you're storing raw, pre-processed, and processed data in a datalake, it's a good idea to organize the data in a way that makes it easy to manage and query. One common approach is to use a hierarchical directory structure, where the data is organized by year, month, and day. Here's an example of how you could organize the data in a datalake:

+ **Raw data**: The raw data can be stored in a top-level directory called "raw", with subdirectories for each year, month, and day. For example, you could have a directory structure like this:

```
raw/
   year=2022/
      month=01/
         day=01/
            data1.csv
            data2.csv
         day=02/
            data3.csv
            data4.csv
      month=02/
         day=01/
            data5.csv
            data6.csv
         day=02/
            data7.csv
            data8.csv
   year=2023/
      month=01/
         day=01/
            data9.csv
            data10.csv
         day=02/
            data11.csv
            data12.csv
      month=02/
         day=01/
            data13.csv
            data14.csv
         day=02/
            data15.csv
            data16.csv
```
+ **Pre-processed data**: The pre-processed data can be stored in a separate directory called "pre-processed", with a similar directory structure as the raw data. For example, you could have a directory structure like this:

```
preprocessed/
   year=2022/
      month=01/
         day=01/
            data1_preprocessed.csv
            data2_preprocessed.csv
         day=02/
            data3_preprocessed.csv
            data4_preprocessed.csv
      month=02/
         day=01/
            data5_preprocessed.csv
            data6_preprocessed.csv
         day=02/
            data7_preprocessed.csv
            data8_preprocessed.csv
   year=2023/
      month=01/
         day=01/
            data9_preprocessed.csv
            data10_preprocessed.csv
         day=02/
            data11_preprocessed.csv
            data12_preprocessed.csv
      month=02/
         day=01/
            data13_preprocessed.csv
            data14_preprocessed.csv
         day=02/
            data15_preprocessed.csv
            data16_preprocessed.csv
```

+ **Processed data**: The processed data can be stored in a separate directory called "processed", with a similar directory structure as the raw data and pre-processed data. For example, you could have a directory structure like this:

```
processed/
   year=2022/
      month=01/
         day=01/
            data1_processed.csv
            data2_processed.csv
         day=02/
            data3_processed.csv
            data4_processed.csv
      month=02/
         day=01/
            data5_processed.csv
            data6_processed.csv
         day=02/
            data7_processed.csv
            data8_processed.csv
   year=2023/
      month=01/
         day=01/
            data9_processed.csv
            data10_processed.csv
         day=02/
            data11_processed.csv
            data12_processed.csv
      month=02/
         day=01/
            data13_processed.csv
            data14_processed.csv
         day=02/
            data15_processed.csv
            data16_processed.csv
```

### Apache Hive

Apache Hive is a tool that is built on top of Hadoop and is designed to allow you to query and analyze data stored in HDFS or other distributed storage systems. **Hive provides a SQL-like language called HiveQL to query data**, and it is able to take advantage of the distributed processing capabilities of Hadoop to perform queries at scale.

One of the key features of Hive is its ability to create schemas for files stored on HDFS. When you create a table in Hive, you define the schema of the table, including the column names, data types, and any other metadata that is required. **Hive then maps the columns in the table to the columns in the underlying data files stored on HDFS**, based on the file format and the data in the files.

Hive **supports a wide range of file formats, including CSV, JSON, Avro, ORC, and Parquet**. Each file format has its own way of storing data, and Hive is able to interpret the data in the files and create schemas for the tables based on the file format.

For example, if you have a CSV file stored on HDFS that contains customer data, you can create a table in Hive that maps to the columns in the CSV file. Here is an example HiveQL statement that creates a table based on a CSV file stored on HDFS:

```
CREATE TABLE customers (
    id INT,
    name STRING,
    email STRING,
    age INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
STORED AS TEXTFILE
LOCATION '/path/to/csv/file';
```

And then you can query the CSV file data as regular SQL queries.

### Apache Hive Components

Hive have multiple components, such as:

+ **Hive Metastore**: The Hive Metastore is a central repository that stores metadata information about Hive tables, including the table schema, column names, data types, and partitioning information. The Metastore stores this metadata in a relational database, such as MySQL, Oracle, or PostgreSQL. By separating the metadata from the actual data stored on HDFS, Hive is able to provide a level of abstraction that allows users to query and analyze data using SQL-like syntax, without having to worry about the underlying storage system.
+ **Hive Query Processor**: The Hive Query Processor is responsible for translating HiveQL queries into MapReduce or Tez jobs that can be executed on a Hadoop cluster. The Query Processor parses the HiveQL queries, performs optimization, and generates a query plan that is optimized for distributed processing.
+ **Hive Execution Engine**: The Hive Execution Engine is responsible for executing the MapReduce or Tez jobs generated by the Query Processor. The Execution Engine manages the distribution of the jobs across the nodes in the Hadoop cluster and ensures that the jobs are executed in a fault-tolerant and scalable manner.
+ **Hive CLI and Beeline**: The Hive CLI (Command Line Interface) and Beeline are command-line tools that allow users to interact with Hive using a command-line interface. The Hive CLI is an interactive shell that allows users to enter HiveQL commands and receive the results directly in the shell. Beeline is a JDBC client that can be used to connect to Hive from external tools and applications.
+ **Hive Drivers and APIs**: Hive provides a variety of drivers and APIs that allow developers to integrate Hive with external tools and applications. These drivers and APIs include JDBC, ODBC, and Thrift, and they allow developers to use Hive as a data warehousing tool for a wide range of use cases.

![Docker-Python](documentation_images/data-lake-10.jpeg)


First let's start the containers from the docker-compose.yml with following command:

```
docker-compose up -d
```

The docker-compose command will start sic containers that has a Hadoop YARN containerized environment with hive integration-

## Step 2

### Spark RDDs

**Spark RDDs (Resilient Distributed Datasets)** are immutable distributed collections of objects that can be processed in parallel.

### Spark Context

**Spark Context** is the entry point for any Spark functionality. It provides a way to interact with a Spark cluster and create RDDs.

### Data Processing

Spark supports two main types of operations:

+ **Transformations**: Transformations are operations that create a new RDD from an existing RDD. Examples of transformations include map, filter, and reduceByKey.
+ **Actions**: Actions are operations that trigger the execution of a Spark job and return results to the driver program. Examples of actions include collect, reduce, and count.

Now let's create a bash session to python_app with following command:

```
docker-compose exec python_app bash
```

Once in the container's bash session, then move to code directory with following command:

```
cd code
```

Now run **clinic_rdd** python file with following command:

```
python clinic_rdd.py
```

This python script uses spark RDDs to load into clinic_db the csv data from clinic_1.csv

### Spark DAG

A DAG (Directed Acyclic Graph) in Spark refers to the sequence of stages and tasks that are executed in a specific order to complete a Spark job.

**Every time an action is executed, Spark internally optimizes the execution or DAG flow to achieve the result.**

## Step 3

### Spark Dataframes

**Spark DataFrames** are a higher-level abstraction built on top of RDDs (Resilient Distributed Datasets) that provide a more convenient and efficient way to work with structured and semi-structured data. **They are conceptually similar to tables in a relational database or data frames in R or Python Pandas**.

Now run **clinic_dataframes** python file with following command:

```
python clinic_dataframes.py
```

This python script uses spark Dataframes to load into clinic_db the csv data from clinic_2.csv

## Step 4

### Spark SQL

**Spark SQL** is a library in Apache Spark that provides a programming interface for working with structured and semi-structured data using SQL-like syntax. It enables users to query and manipulate data using SQL statements and provides support for executing SQL queries on top of Spark data sources, including Hive, Avro, Parquet, ORC, JSON, and JDBC.

Spark SQL can be used with both DataFrames and RDDs. When using DataFrames, Spark SQL provides a more convenient way to query and manipulate data using SQL-like syntax. DataFrames can be registered as temporary tables or global tables, which can then be queried using SQL statements. Spark SQL also provides support for window functions, user-defined functions (UDFs), and streaming data.

Now run **clinic_sparksql.py** python file with following command:

```
python clinic_sparksql.py
```

This python script uses Spark SQL to load into clinic_db the csv data from clinic_3.csv


## Conclusion

In summary, a datalake is a centralized repository for storing and managing large volumes of data, and it can be implemented using HDFS and Hive to provide a scalable and fault-tolerant storage and querying solution for big data analytics and data science projects.

