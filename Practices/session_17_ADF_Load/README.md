# Extract and Load: Azure Data Factory

In previous practice we provisioned our environment with all resources required for ELT, in this practice we will be doing the EL part from the ELT.

>Azure calls this part (Load) *"Copy"*
>
>We will be using different sources to copy to a database or datawarehouse

## What you will learn

* Azure Data Factory workspace
* How to LOAD data from a datalake into database
* How to LOAD data from a HTTP source into a DB
* How to LOAD data from a DB into a DW
* How to TRANSFORM data types with Data Flow activities in ADF
* How to LOAD data from a datalake into Snowflake (Optional)

## Practice

### Requirements

You are a data engineer working for a credit rating agency. You need to:

* Get Stock Market Data every day
* Store it in a Data Warehouse for financial research and analysis for further publication.

>You work in the team responsible of getting Nasdaq data from different resources or formats.

### Step 0 - Launch ADF Studio

On your azure portal

* Go to **All Resources**
* Select the data factory you created in the past session
* Click on **Launch Studio**

![img](documentation_images/ADF_launch_studio.png)

Remember that for each **Copy** activity, we will create a source dataset and a sink dataset.

### Step 1 - ADF Copy Activities

#### Copy from datalake to database

* Once in the Data Factory Studio, on your most left panel, select **Author**

  ![img](documentation_images/ADF_left_panel.png)
* Click ... con **Pipelines** and create a new pipeline
* Under the **Activities** panel, select and drag **Copy data**

  ![img](documentation_images/New_activity_adf.png)
* On the most right panel, select a name for your pipeline, similar to "csv_to_db_pl" or any name
* Under the workspace area you will find all the configurations for your activity. You can set any name for your activity

  ![img](documentation_images/ADF_activity_config.png)
* Go to Source in the activity configurations and create a new source dataset
* Search for **Azure Blob Storage**, then select **DelimitedText**
* Select a name for your dataset, could be "AAPL_csv_ds" (you can also rename datasets later)
* Select the **Linked service** for Blob Storage created in the past session, similar to "blobdata101_ls"
* Browse for the file called "AAPL.csv" in the "data" folder
* Check the box for **First row as header**
* On **Import schema** you can import from connection/store or select none (later you can import the schema as well)
* Click **OK**
* On the activity configurations, go to **Sink** and create a new dataset
* Search for **Azure SQL Database**
* Set a name for your dataset ("AzureSQLTable_AAPL_landing_ds"), select the linked service for the azure db you created in the past session
* Select "dbo.AAPL_landing" table
* You can import the schema or import it later
* Under your activit configurations go to **Mapping** and **Import schemas** (so you can view mapping/transformation options)

  ![img](documentation_images/ADF_mapping_schemas.png)
* For fixed or known schemas it is usefull to import the schemas and review or modify your mappings. Here you can also preview the data (not all sources allow data preview).
* In this case, **Clear** the schema (at this moment we will not make any transformation since we are building ELT pipelines)
* If everything looks like expected, on the upper tabs of your workspace, click **Validate** and if there are no errors, click on **Publish** (saves the pipeline in your Data Factory workspace) and then **Debug** or **Trigger now**

#### Copy from http to database

* Create a new pipeline, set a propper name
* Drag a new **Copy data** activity
* Go to Source in the activity configurations and create a new source dataset
* Search for **HTTP**, then select **DelimitedText**
* Select a name for your dataset, could be "http_fredGDP_csv_ds" (you can also rename datasets later)
* Select the **Linked service** for http created in the past session, similar to "nasdaq_http_ls"
* Enter the following relative url: \
  `api/v3/datasets/FRED/GDP.csv?collapse=annual&order=asc&column_index=1`
* Check the box for **First row as header**
* On **Import schema** you can import from connection/store or select none (later you can import the schema)
* Click **OK**
* On the activity configurations, go to **Sink** and create a new dataset
* Search for **Azure SQL Database**
* Set a name for your dataset ("AzureSQLTable_FREDGDP_landing_ds"), select the linked service for the azure db you created in the past session
* Select "dbo.FRED_GDP_landing" table
* You can import the schema or import it later
* Under your activit configurations go to **Mapping**
* If everything looks like expected, on the upper tabs of your workspace, click **Validate** and if there are no errors, click on **Publish** (saves the pipeline in your Data Factory workspace) and then **Debug** or **Trigger now**
* Nasdaq Data Link API: [info](https://docs.data.nasdaq.com/docs/time-series), [rate/limits](https://docs.data.nasdaq.com/docs/rate-limits)

#### Copy from database to data warehouse

* Create a new pipeline, set a propper name
* Drag a new **Copy data** activity
* Go to Source in the activity configurations and select the dataset you created as sink for Azure DB ("AzureSQLTable_AAPL_landing_ds") in the previews steps
* Leave the defaults
* Go to **Sink** tab and create a new dataset
* Search for **Azure Synapse Analytics**
* Set a name for your dataset, could be "AAPL_dw_ds" (you can also rename datasets later)
* Select the linked service for the DW you created in the past session ("adventureworks_dw_ls")
* Select "AAPL_landing" table
* Do not import schema and click **OK**
* Click **Validate** and if there are no errors, click on **Publish** (saves the pipeline in your Data Factory workspace) and then **Debug** or **Trigger now**
* Go to Data Studio or SMSS, create a new query for your "AdventureWorksDW" and run:

  ```sql
  SELECT TOP 100 * FROM dbo.AAPL_landing;
  ```

* DELETE: Once you can view the data in your DW, on your Azure portal, go to **All resources** select and delete "AdventureWorksDW" resource to keep the cost at the minimum.

### Step 2 - ADF Transformations

We will do some simple transformations using data flow activity in ADF. This transformations will convert the data types from the landing tables to the precise types in the final table.

This could also be achieved with a sql script, but for this session we will use the Azure Data Factory GUI.

>Keep in mind that there is not just one way to build a pipeline. It will depend on your business needs and resources available.

#### Data Flow (AAPL)

In your ADF workspace:

* Create a new pipeline and drag a **Data Flow** activity.
  >You could also add the activity in the "copy_from_csv_to_db_pl" pipeline so it would run the transformation inmediatly after the LOAD process. If you choose the second option it should look like this:

  ![img](documentation_images/Load_transform_pipeline.png)
* Click on the Data flow activity
  * In the tabs that appear below
  * Select **Settings**
  * Click **New**

  ![img](documentation_images/New_dataflow_transform_1.png)
* Select **Add Source**

  ![img](documentation_images/Add_source_dataflow.png"  width=25% height=25%>
* On **Source settings**
  * Select the dataset "AzureSqlTable_AAPL_ds"
  * Leave the defaults

  ![img](documentation_images/Source_settings_dataflow.png)
* On the **Projection** tab you can preview the schema and data types

  ![img](documentation_images/Source_projection_transform1_adf.png)
* Click on the + icon beside the source image
  * Select **Cast**:

  ![img](documentation_images/+_cast.png)
* On the **Cast settings** tab make sure to set everything as the image below

  ![img](documentation_images/Transform_1_adf.png)
* Now click the **+** and select **Sink**
* Under the **Sink settings** set the corresponding values:
  ![img](documentation_images/New_sink_dataset_transform_1.png)
  * You will need to create a New dataset using the SQL Database linked service and selecting "AAPL" table.

#### Data Flow (FRED_GDP)

We will add another flow in the same activity. It will be the same as the above but for FRED_GDP data. This could be done in separate activities, but it is important to aknowledge the capacities of this tool. In fact, in ELT processes and datawarehousing many transformations involve more than one source, like when creating a Fact or a Dim table in a DW, or you just need a Join or a Lookup or other functions in your transformation pipeline and more than one source is required.

* Add another source:
  
  ![img](documentation_images/Add_source_transform2.png)

* Now select the FredGdp dataset
* Add a **Cast** step
  >**Important**: Under **Cast settings**, make sure that you select the correct date format for casting. \
  >Check your FRED_GDP dataset or the csv file in the Blob Storage for the adequate date format.
* Create a sink dataset selecting "FRED_GDP" table
* Now you can go to the pipeline and **Trigger now**
* You can go to SSMS or Data Studio and run

  ```sql
  SELECT TOP 100 * FROM dbo.AAPL;
  ```

  And then

  ```sql
  SELECT TOP 100 * FROM dbo.FRED_GDP;
  ```

  You have succesfully completed this transformations!

>**Data flow** activities in ADF are very useful and efficient for low complexity transformations. However, for high complexity transformations, it is recomended to use Spark on Synapse or Spark on Databricks or other specialized tool for transformations.

### Step 3 - Load to Snowflake (Optional)

#### Copy from datalake to snowflake

* Make sure you have in your snowflake database the following table:

  ```sql
  CREATE TABLE products_adf (
      id int,
      name varchar(500),
      description varchar(500),
      price varchar(50),
      stock varchar(50)
  )
  ```

* Create a new pipeline, set a propper name
* Drag a new **Copy data** activity
* Go to Source in the activity configurations and create a new source dataset
* Search for **Azure Blob Storage**, then select **DelimitedText**
* Select a name for your dataset, could be "snowflake_data_csv_ds" (you can also rename datasets later)
* Select the **Linked service** for Blob Storage created in the past session, similar to "blobdata101_ls"
* Browse for the file called "products_2015.csv" in the "data" folder
* Check the box for **First row as header**
* On **Import schema** you can import from connection/store or select none (later you can import the schema)
* Click **OK**
* On the activity configurations, go to **Sink** and create a new dataset
* Search for **Snowflake**
* Set a name for your dataset ("Snowflake_data__sink_ds"), select the linked service for snowflake you created before
* Fill in the correct values
* Under your activit configurations go to **Mapping** and mapp the id to integer in your destination schema, the rest should be strings
* If everything looks like expected, on the upper tabs of your workspace, click **Validate** and if there are no errors, click on **Publish** (saves the pipeline in your Data Factory workspace) and then **Debug** or **Trigger now**
* You can go to your Snowflake account and you will find your data there!

## Still curious

* In this lesson we use ADF, but how it compares to AWS and GCP?

  Azure Data Factory: \
  Azure Data Factory is a cloud-based data integration service that allows you to create, schedule, and manage data-driven workflows.

  * ETL Capabilities: Supports Extract, Transform, Load (ETL) processes for data movement and transformation.
  * Data Orchestration: Provides data orchestration capabilities to schedule and automate data pipelines.
  * Data Integration: Integrates with Azure services such as Azure Blob Storage, Azure SQL Data Warehouse, and more.
  * Data Flow: Offers Data Flow for visual data transformation and transformation logic.
  * Hybrid Cloud: Strong support for hybrid cloud scenarios with Azure Stack.
  * Integration: Integrates well with Microsoft ecosystem and services.

  AWS Glue: \
  AWS Glue is a managed ETL (Extract, Transform, Load) service that automates data preparation and transformation tasks.

  * ETL Capabilities: Focuses on ETL processes and provides a serverless environment for data transformation.
  * Crawling and Cataloging: Can automatically discover and catalog metadata from various data sources.
  * Data Lake Integration: Well-suited for integration with AWS data lakes and services like Amazon S3, Amazon Redshift, and more.
  * Data Catalog: Includes AWS Glue Data Catalog for storing metadata information.
  * Serverless: Provides serverless execution of ETL jobs.

  Google Cloud Dataflow: \
  Google Cloud Dataflow is a fully managed stream and batch data processing service.

  * Batch and Stream Processing: Supports both batch and stream data processing for real-time and batch workloads.
  * Apache Beam: Dataflow is built on Apache Beam, an open-source unified stream and batch processing model.
  * Data Transformation: Enables data transformation and processing at scale.
  * Serverless: Offers serverless and auto-scaling capabilities.
  * Integration: Integrates with Google Cloud services like BigQuery, Cloud Storage, and Pub/Sub.
  * Dataflow SQL: Allows querying and processing data using SQL-like queries.

* Still want more information:

  * Article: [Compare AWS Glue vs. Azure Data Factory][glue_vs_adf]
  * Article: [Comparing Major Cloud Service Providers][comparing]
  * [Official Azure guide for ETL][azure_etl]

## Links

* [Compare AWS Glue vs. Azure Data Factory][glue_vs_adf]
* [Comparing Major Cloud Service Providers][comparing]
* [Official Azure guide for ETL][azure_etl]

[glue_vs_adf]: https://www.techtarget.com/searchcloudcomputing/tip/Compare-AWS-Glue-vs-Azure-Data-Factory
[comparing]: https://datatechinsights.hashnode.dev/comparing-major-cloud-service-providers-aws-vs-azure-vs-google-cloud
[azure_etl]: https://learn.microsoft.com/en-us/azure/architecture/data-guide/relational-data/etl
