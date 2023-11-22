# SQL Reporting

You will learn about sql querying for data reporting with external tables ELT.

## Prerequisites

* Follow the [pre-setup guideline][pre-setup]

## What will you learn

* AWS
  * CLI with S3
  * Roles
* Snowflake
  * Data integration
  * Stages
  * External Tables
  * Foreign Keys on OLAP
  * Views

* ELT
* Normalize the data into a Star or Snowflake Schema
* Views

## Practice

Get the data ready to query using an external table

### Requirements

Use the generator data to:

* Generate data
* Use the AWS CLI to move data to S3
* Connect S3 to Snowflake
  * Create fact and dimensions as needed using `sql`
  * Fill the fact/dimensions using `external table`

### Step 0 - Bucket

* Create a Bucket named `de-101-session-12`

>We already created a bucket in a [previous session][create_bucket], this is the same process
>
>For this session, the bucket will be already created

### Step 1 - Generator

>The bucket already contains some data, but let's generate some additional data

* Run `python3 practice_files/generator.py -y 2023 -r 1 -c amazon --hdfs` \
  This will create data for year 2023, for the amazon company, but you use instead your own name (ex. enrique-garcia, jesus-gaona)

> You can check more options with the `-h` flag

### Step 2 - AWS CLI

>We can upload the files using the AWS Console, but if we plan to implement the process as part of CI/CD we need to use the AWS CLI

* Configure keys

  `aws configure --profile de-101-student` or `aws configure --profile de-101-student-ext`

  * Fill the information as requiered
    * `AWS Access Key ID [None]`: \<Given by the instructor>
    * `AWS Secret Access Key [None]`: \<Given by the instructor>
    * `Default region name [None]`: us-east-1
    * `Default output format [None]`: json

This will create `config` and `credentials` files in:

* Linux/Mac: `~/.aws`
* Windows: `%USERPROFILE%\.aws\`

[Location of the shared config and credentials files][config_file_location] \
[AWS CLI Command Reference: configure][aws_config_reference]

#### 2.1 - AWS S3 CLI

* Move to the `practice_files` folder
* Upload folder to bucket

```sh
aws s3 sync generated_data s3://de-101-session-12/generated_data/ --profile de-101-student
```

|parameter|explanation|
|-|-|
|aws|aws cli|
|s3|aws module|
|generated data|Local folder path|
|s3://de-101-session-12/generated_data/|Cloud folder path|
|--profile|Flag to pass a permission profile|
|de-101-student|Profile name|

### Step 3 - AWS Role

>Follow these steps in instructor screen

In the AWS Console

* Go to IAM > Roles > Create Role
  * AWS Account
    * This acount
      >We will modify this later
    * External Id: `external-id-placeholder`
      >We will be using a placeholder and will return later
  * Permissions
    * Policy: `de-101-rw-s3`
      >This policy must have read permissions over the bucket from the previous step
  * Name and Review
    * Name: `de-101-external-s3-db`

### Step 4 - Snowflake S3 Integration

Go to snowflake, then:

* Use correct role \
  `accountadmin` is the only profile who has capabilities to create integrations

  ```sql
  USE ROLE accountadmin;
  ```

* Create storage integration

  ```sql
  CREATE STORAGE INTEGRATION enroute_s3
    TYPE = EXTERNAL_STAGE
    STORAGE_PROVIDER = S3
    STORAGE_AWS_ROLE_ARN = '<AWS_ROLE_ARN>'
    ENABLED = TRUE
    STORAGE_ALLOWED_LOCATIONS = ('<S3_BUCKET_AND_PATH_URI>');
  ```

### Step 5 - AWS Role Tuning

>Follow these steps in instructor screen

* Get information from snowflake
  
  ```sql
  DESCRIBE INTEGRATION enroute_s3;
  ```

  Save the fields `STORAGE_AWS_IAM_USER_ARN` and `STORAGE_AWS_EXTERNAL_ID`

* In IAM > Roles
* Search the role we created on previous step: `de-101-external-s3-db`
* Trust Relationships
  * Edit `STORAGE_AWS_IAM_USER_ARN`

    ```json
    "AWS": "arn:aws:iam::############:root"
    ```

  * Change to

    ```json
    "AWS": ["arn:aws:iam::704308174698:user/87pd0000-s"]
    ```

  * Edit `STORAGE_AWS_EXTERNAL_ID`

    ```json
    "sts:ExternalId": "external-id-placeholder"
    ```

  * Change to

    ```json
    "sts:ExternalId": ["BO94478_SFCRole=2_KgrNiKXW4+YTBnG5c63rG3IxgVU="]
    ```

* Save policy

>In order to include your credentials too send `STORAGE_AWS_IAM_USER_ARN` and `STORAGE_AWS_EXTERNAL_ID` to Teacher Assistant via Keybase, the message should explode in 7 days
>
>Message template:
>`STORAGE_AWS_IAM_USER_ARN`: <STORAGE_AWS_IAM_USER_ARN>
>`STORAGE_AWS_EXTERNAL_ID`: <STORAGE_AWS_EXTERNAL_ID>

### Step 6 - External table

* Create a database if not exists

  ```sql
  CREATE DATABASE fundamentals_db;
  USE fundamentals_db;
  ```

* Create stage

  ```sql
  CREATE OR REPLACE STAGE stage_enroute
    STORAGE_INTEGRATION = enroute_s3
    URL = 's3://de-101-session-12/generated_data/'
    FILE_FORMAT = (
      TYPE = 'CSV'
      FIELD_OPTIONALLY_ENCLOSED_BY = '"'
      SKIP_HEADER = 1
    );
  ```

  * You can verify the stage has correct access

    ```sql
    LIST @stage_enroute;
    ```

* Create External Table

  ```sql
  CREATE OR REPLACE EXTERNAL TABLE ext_product (
    name VARCHAR AS (value:c1::VARCHAR),
    category VARCHAR AS (value:c2::VARCHAR),
    brand VARCHAR AS (value:c3::VARCHAR),
    price DOUBLE AS (value:c4::DOUBLE),
    sales DOUBLE AS (value:c5::DOUBLE),
    company VARCHAR AS (value:c6::VARCHAR),
    year NUMBER AS (value:c7::NUMBER),
    month NUMBER AS (value:c8::NUMBER),
    state VARCHAR AS (value:c9::VARCHAR)
  )
  LOCATION = @stage_enroute
  FILE_FORMAT = (
    TYPE = 'CSV'
    SKIP_HEADER = 1
  )
  AUTO_REFRESH = TRUE;
  ```

* Query External table

  ```sql
  SELECT * FROM ext_product LIMIT 100;
  ```

### Step 7 - Fact and Dimension

On previous session we addressed the facts and dimension tables, let's create a Star Schema for this database

#### 7.1 - Fact

As we discussed on another topic the `fact table represents the main concept that the whole schema will move around`, in this case `sales`

* Identify fields and usage \
  If we think in sales as a ticket the ticket should contain:

  * The product we are selling
  * The company selling that product
  * The sales date
  * The state where the sale occurs
  * The individual price
  * The full sale price
  * A ticket Id

* Identify those that would can't reused for different tickets
  * `individual price`: this is unique because discount can occur per item, per date, customer type...
  * `sale price`: this is unique because it depends on offers, discounts per cart, date, combos...
  * `ticket id`: this wraps the two values above with the other fields being a direct access to the record

* Identify reusable fields
  * `product`: the same product can be sold multiple times depending on available inventory
  * `company`: a company can have multiple products
  * `sales date`: the year/month/day/hour even sometimes the second can have multiple sales at the same time (multiple stores, cashiers...)
  * `state`: a company can have the same selling product on different states

* Create the table \
  We will use these unique fields as properties of the fact table and reusable fields as foreign keys (a foreign key will wrap all related data making fact table cleaner)

    ```sql
    CREATE TABLE fact_sale (
      sales_key INT PRIMARY KEY,
      date_key INT,
      state_key INT,
      product_key INT,
      company_key INT,
      price DOUBLE,
      sales DOUBLE
    );
    ```

  >We can't create now the FK since we don't have dimension tables, we will modify this later

#### 7.2 - Dimensions

These will contain all non unique data from the sale

* Create the tables

  ```sql
  CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    year NUMBER,
    month NUMBER
  );

  CREATE TABLE dim_state (
    state_key INT PRIMARY KEY,
    state VARCHAR
  );

  CREATE TABLE dim_product (
    product_key INT PRIMARY KEY,
    name VARCHAR,
    category VARCHAR,
    brand VARCHAR
  );

  CREATE TABLE dim_company (
    company_key INT PRIMARY KEY,
    company VARCHAR
  );
  ```

#### 7.3 - Foreign Keys

>As we mention the fact is related to the dimensions, however `adding foreign keys can be not always the best option in a OLAP system`, this is for 2 main reasons:
>
>* `Sanity`: If data is not accurate or contains errors, we can cause errors during the insert slowing the insertion process for a troubleshoot or in worst scenario leading data loss
>* `Performance`: Even if the data is sanitized properly, having a foreign key consumes resources, a `1 second delay for 1 000 records means minutes in billions of records`
>
>For these 2 reasons only use FK when you are sure they will not hinder your performance, you trust the sanitization process 100% or for documentation purpouses

In this scenario we will create the FK but they will not be enforced, this is because the data has not passed a sanitization process

* Create FK

  ```sql
  ALTER TABLE fact_sale ADD FOREIGN KEY (date_key) REFERENCES dim_date (date_key) NOT ENFORCED;
  ALTER TABLE fact_sale ADD FOREIGN KEY (state_key) REFERENCES dim_state (state_key) NOT ENFORCED;
  ALTER TABLE fact_sale ADD FOREIGN KEY (product_key) REFERENCES dim_product (product_key) NOT ENFORCED;
  ALTER TABLE fact_sale ADD FOREIGN KEY (company_key) REFERENCES dim_company (company_key) NOT ENFORCED;
  ```

#### 7.4 - Fill tables

As we mention with the fact table id this is a hashlike value unique to the record, the same applies for all other PK in the dimensions

* Fill data in Dimensions tables

  ```sql
  INSERT INTO dim_date (date_key, year, month)
  SELECT DISTINCT
    year * 10000 + month * 100 + RANK() OVER (ORDER BY year, month) AS date_key,
    year,
    month
  FROM ext_product;

  INSERT INTO dim_state (state_key, state)
  SELECT DISTINCT
    RANK() OVER (ORDER BY state) AS state_key,
    state
  FROM ext_product;

  INSERT INTO dim_product (product_key, name, category, brand)
  SELECT DISTINCT
    RANK() OVER (ORDER BY name) AS product_key,
    name,
    category,
    brand
  FROM ext_product;

  INSERT INTO dim_company (company_key, company)
  SELECT DISTINCT
    RANK() OVER (ORDER BY company) AS company_key,
    company
  FROM ext_product;
  ```

* Fill data in Fact table

  ```sql
  INSERT INTO fact_sale (sales_key, date_key, state_key, product_key, company_key, price, sales)
  SELECT
    ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS sales_key,
    d.date_key,
    s.state_key,
    p.product_key,
    c.company_key,
    e.price,
    e.sales
  FROM ext_product e
  JOIN dim_date d ON e.year = d.year AND e.month = d.month
  JOIN dim_state s ON e.state = s.state
  JOIN dim_product p ON e.name = p.name
  JOIN dim_company c ON e.company = c.company;
  ```

## Homework

* Generate the required querys
  * Don't mix Companies in your results.
  * Store in `create_views.sql` in your local branch if needed

1. Select the price and product for every state and month
2. Select the amount of sales by product-year for every state
3. Select the month with the highest sales for every product
4. Select the month with the lowest sales for every product
5. Get the most sold category for every company
6. Get the total sales (in money) for a company in every state

### Optional

* What would you change to make this a Snowflake schema?
* Do you think that would improve or hinder the performance?
  * Why?

>Hint: It could be possibly that product contains a column that can be reused

* Use the AWS CLI to navigate the bucket and print the content of any of your uploaded csv files to the console
* Investigate why is a good practice to always use the `--profile` option when using the AWS CLI

## Still curious

You want more SQL exercises?

* [Exercism PL/SQL][exercism]
* [HackerRank SQL][hackerrank]
* [Letetcode Database][leetcode]

Improve your SQL readability:

* [10 Best Practices to Write Readable and Maintainable SQL Code][sql_good_practices]
* [Best practices for writing SQL queries][sql_best_practices]

## Links

### Used during this session

* [Pre-Setup][pre-setup]
* [Exercism PL/SQL][exercism]
* [HackerRank SQL][hackerrank]
* [Letetcode Database][leetcode]
* [10 Best Practices to Write Readable and Maintainable SQL Code][sql_good_practices]
* [Best practices for writing SQL queries][sql_best_practices]

### Session reinforment and homework help

* [Best practices to use AWS access key and secret in your development environment][aws_best_practices]
* Documentation: [Configuration and credential file settings][aws_config]
* [Everything you need to know about AWS CLI Profiles][cli_profiles]
* Documentation: [Working with External Tables][ext_tables]
* Documentation: [AWS CLI Command Reference][awscli_reference]

[pre-setup]: ./pre-setup.md

[create_bucket]: ../session_6_intro_cloud_airflow/README.md#step-1---s3-bucket

[config_file_location]: https://docs.aws.amazon.com/sdkref/latest/guide/file-location.html
[aws_config_reference]: https://docs.aws.amazon.com/cli/latest/reference/configure/
[awscli_reference]: https://docs.aws.amazon.com/cli/latest/
[exercism]: https://exercism.org/tracks/plsql/exercises
[hackerrank]: https://www.hackerrank.com/domains/sql
[leetcode]: https://leetcode.com/problemset/database/
[sql_good_practices]: https://towardsdatascience.com/10-best-practices-to-write-readable-and-maintainable-sql-code-427f6bb98208
[sql_best_practices]: https://www.metabase.com/learn/sql-questions/sql-best-practices

[aws_best_practices]: https://dev.to/sahays/best-practices-to-use-aws-access-key-and-secret-in-your-development-environment-23ki
[aws_config]: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
[cli_profiles]: https://dev.to/andreasbergstrom/juggling-multiple-aws-cli-profiles-like-a-pro-2h88
[ext_tables]: https://docs.snowflake.com/en/user-guide/tables-external
