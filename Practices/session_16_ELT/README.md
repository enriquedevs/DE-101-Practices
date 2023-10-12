# ELT Environments and Database Integration

In this practice we will setup the environment, tools and resources necesary for the following sessions.

## Prerequisites

* Azure Free Account ([Instructions][azure_pdf])
* Azure Data Studio or SQL Server Management Studio
  * [Data Studio for MacOS][sql_server_mac]
  * [SSMS for Windows][sql_server_win]
* OpenWeather API key: [Create free account][openweather_api]

## What you will learn

* Overview of Microsoft Azure
* How to create resources on Azure Portal
* How to connect to a Database in Azure with Data Studio or SSMS
* Azure Data Factory (ADF) linked services
* Linked service: Snowflake (optional)

## ETL VS ELT

In general the advantages of ETL are the advantages of ELT

|-|ETL| ELT|
|-|-|-|
|Transformations|Non-sql code dedicated stage|Limited to SQL after insert or during query execution|
|Data Quality|Done during transformation, inserted data is clean|Limited to table constraints, data inserted is raw|
|Integration with Other Systems|Requires manual integration, but support what you can code|Limited to Database connectors|
|Pipeline time|Slow: information not available until transformation is done|Real time/near real time: pipeline work as a bridge|
|Scalability|Harder to manage as input increases|Only need more space in the destiny database|
|Costs|Processing|Storage (and processing when doing complex querys)|

>Since ETL performs the transformations during pipeline this means data may not be available ASAP, also it requires additional resources such as intermediate data structures that can increase the complexity of the pipeline, however well managed these structures can be refined to make efficient datamarts in the same step and increase data quality.
>
>ELT on the other side will only do simple transformations, but will give you the data ASAP. It's worth notice that ELT may look like never do the transformation part, but it performs the transformation after being stored or during execution time.

[![img](documentation_images/ETL-Process.png)][etl_vs_elt]

## Practice

You are a data engineer working for a credit rating agency. You need to:

* Get Stock Market Data every day
* Store it in a Data Warehouse for financial research and analysis for further publication.

You work in the team responsible of getting Nasdaq data from different resources or formats.

### STEP 1 - Set the playground

#### Resource Group

>A resource group is a logical container that holds related Azure resources such as virtual machines, databases, storage accounts, virtual networks...

* In your Azure portal, type in and select "Resource groups"

  ![img](documentation_images/resource_group.png)
* Select **+ Create** and follow the instructions. Name suggested similar to "data-eng-101-rg"
* Region: remember that all your resources should be in the same region. In this course, for those in Mexico, South Central US is recommended. Leave the rest with the defaults. Go to **Review + create** and click **Create**.

#### Resource Providers

>Resource providers enable the provisioning, management, and maintenance of Azure resources or services, such as virtual machines, databases, storage accounts, networking...

* On the azure portal, type in and Select **Suscriptions**, select yours and then on the left panel **Resource Providers**
* Type in Synapse, select the row and click **Register**

  ![img](documentation_images/synapse_resource_provider.png)
* Make sure to have the following providers registered

  [img](documentation_images/azure_resource_providers.png)

#### Blob Storage

>Blob Storage is the cloud storage for azure, it allows you to store images, logs. videos, backups...

* In the search bar, type in and select "Storage accounts"
* Select **+ Create** and choose the resource group you just created
* Type a name for your storage account. It could be similar to "blobdata101abc"
* Select the same region as your resource group
* Performance: **Standard**
* Redundancy: **Locally-redundant storage (LRS)**
* Leave the rest with the defaults and **Create**
* Go to **All Resources** in your Azure portal and select this storage account
* On the left panel, click on **Containers** and then **+ Create**
* Set any name. Suggested "data"
* Public access level: **Container(...)**
* Then go to the created container and click **Upload** from the tabs section and upload "AAPL.csv" from the blob_data folder in this session (git repo)

#### Data Lake Storage

>Azure Data Lake Storage is a cloud-based data lake solution provided by Microsoft Azure. It is designed to store and manage large volumes of structured and unstructured data.

* In the search bar, type in and select "Storage accounts"
* Select **+ Create** and choose the resource group you just created
* Type a name for your storage account. It could be similar to "blobdata101abc"
* Select the same region as your resource group
* Performance: **Standard**
* Redundancy: **Locally-redundant storage (LRS)**
* Go to **Advanced** tab and in the **Data Lake Storage Gen 2** section, check the box **Enable hierarchical namespace**  
* Leave the rest with the defaults and **Create**  
* Go to **All Resources** in your Azure portal and select this storage account
* Create one container: "data"
* Create two folders inside your container: "raw", "processed"

#### SQL Server

>SQL Server is the Microsoft approach for RDBMS

* Type in and select "SQL servers"
* Select **+ Create** and follow the instructions
* Set a server name. Suggested similar to "data101-srv-abc"
* Select the same region as your resource group
* Authentication: seletc **SQL Authentication** and set an admin username and strong password (remember or write down this info for further use)
* Networking: Select **YES** for **Allow Azure services and resources to access this server**
* Leave the rest with defaults and **Create**

#### SQL Database

>SQL Database is the instance of SQL RDBMS

* Type in and select "SQL databases"
* Select **+ Create** and follow the instructions
* Set a database name. Suggested similar to "data101-db"
* Compute + storage : **Basic 5 DTUs**
* Redundancy: **Locally redundant**
* Networking: Add current IP address set to **YES**
* Leave the rest with the defaults and **Create**
* Type in and select **SQL databases** and select this database
* On the left panel, select **Overview** and then on the upper right side copy the Server name
* Go to SSMS or Azure Data Studio, create a new connection
* Server: paste the Server name you copied
* Use the username and password you created while creating the SQL server above
* Leave the defaults and connect

#### Dedicated SQL Pool

>Azure Dedicated SQL Pool, formerly known as SQL Data Warehouse is the datawarehouse solution provided my microsoft

* Type in and select "SQL servers"
* Select **+ New dedicated SQL pool (formerly SQL DW)**
* Name: "AdventureWorksDW"
* Performance level: **DW100c**
* Additional settings tab --> Data source: Sample
* Leave the rest with the defaults and **Create**
* Refresh the connection in SSMS or Data Studio and you should see this DW listed

#### Azure Data Factory (Workspace)

>Azure Data Factory is the Data integration by microsoft, this includes create and manage workflows.
>
>Within Azure Data Factory, a "Workspace" is a logical container or environment where you can create and manage data pipelines, datasets, linked services, triggers, and other assets related to your data integration and transformation tasks.

* Type in and select **Data factories**
* Select **+ Create**
* Select **Resource group** and **Region** the same as all the above
* Set any name. Suggested similar to "data101-abc-df"
* Leave the defaults and **Create**
* Go to **All Resources**, select this data factory and click on **Launch Studio**
* It will open a new page like this:

  ![img](documentation_images/ADF_home.png)

### STEP 2 - Make your connections

In this step we will mount all the resources we created on previous step so they can be usable by our ADF

#### HTTP

* On your ADF workspace, on the left panel select **Manage**, click on **Linked services** and create a new one
* On the search bar, type in and select **HTTP** and set the following values:

  ![img](documentation_images/http_ls.png)
* Base URL: <https://data.nasdaq.com>
* Test connection and create
* Nasdaq Data Link API: [info][nasdaq_timeseries], [rate/limits][nasdaq_rate_limits]

#### Azure Blob Storage

* On your ADF workspace, on the left panel select **Manage**, click on **Linked services** and create a new one
* On the search bar, type in and select **Azure Blob Storage** and set the following values:

  ![img](documentation_images/blob_ls.png)
* Test connection and create

#### Azure Data Lake Storage Gen2

* Redo the steps above but type in and select **Azure Data Lake Storage Gen2**, then fill in the corresponding values

#### Azure SQL Database

* On your ADF workspace, on the left panel select **Manage**, click on **Linked services** and create a new one
* On the search bar, type in and select **Azure SQL Database**, then fill in the corresponding values

#### Snowflake (Optional)

* **Snowflake linked service**
  * On your ADF workspace, on the left panel select **Manage**, click on **Linked services** and create a new one
  * On the search bar, type in and select **Snowflake**
  * Name: "snowflake_ls"
  * Enter your snowflake account ("accountname.southcentral-us.azure")
  * Fill in the values for user, pssw, db, dw
  * Test your connection and create
  
    ![img](documentation_images/ADF_snowflake_ls.png)

## Note

>SQL Server is not available directly for macOS. But you could run it locally with a Docker container:
>
>* SQL Server local instance for macos with Docker: [docker-compose.yml](docker-compose.yml)

## Still curious

### ELT Basics

>ELT (Extraction Load Transform) is a data process method where the data is inserted raw or almost raw into the final destination.

* Why should we consider having raw data in our datawarehouse instead of a normalized tailored data?

  Unlike ETL, where we spend some time normalizing and enriching data, this in some cases is not sustainable:
    >As the volume and data complexity increases the time spent executing and mantaining an ETL increases too

  ELT can help us on this topic, since we can process the data faster, but this also means we can split the data load without breaking constraints enabling even faster processing speeds.

* But we still have a problem, the data is still raw and is complex to query

  The data obtained after ELT it's raw, however nowadays we have tools to manage data catalogs and metadata managers. \
  This essentially means the data is not just an unformatted raw file, but instead an structure we can query

* Ok we can query the data, but that doesn't mean is good data (Quality check)

  With today tools we can enable check at various stages of the ELT pipeline to ensure that data meets specific criteria, such as completeness, consistency, and accuracy. Monitoring can be used to track data quality over time and identify trends and issues.

* We can add on top of it

  Machine Learning and AI can be used to identify patterns, reducing the need for manual intervention; also recommend remediation steps in case of data quality issues prediction.

#### ELT pipelines tools

These are some of the tools you can use to mount your ETL process

* Apache Airflow \
  An open-source platform for programmatically authoring, scheduling, and monitoring workflows
* Talend \
  A data integration and management tool that supports ELT workflows
* AWS Glue \
  A fully managed ETL service that supports both ETL and ELT workflows in the cloud
* Microsoft Azure Data Factory \
  A cloud-based data integration service that supports both ETL and ELT workflows
* Google Cloud Dataflow \
  A cloud-based data processing service that supports both batch and stream processing, including ELT workflows.

### ETL Basics

We already have a lesson on this topic on: [session 5][session_5]

### ELT + ELT = ETLT?

As a tendency in the last years and as companies have more and more data, they slowly start to transition ETL into ELT pipelines, however other engineers are doing hybrid ETL/ELT:

ETL part is used to handle complex transformations and data quality checks while the ELT part takes care of the after insert less complex transformations since the SQL engine can run queries faster than custom datasets by code such as python.

Another problem this approach can solve is to address different issues within the same organization

    Ex. Sales department requires data in real time, while the marketing team requires complex transformations for reports at the end of each shift.

>There's nothing written use the tools available to solve the problem and combine technologies in a way that's logical to avoid future problems

* Have you ever heard about ETLT?
  * Article: [What Is ETLT?][etlt]
* Still not sure when to use ETL over ELT?
  * Article: [ETL vs ELT Flowchart][etl_elt_chart]

## Links

* [ETL vs ELT][etl_vs_elt]
* [Create Azure Account PDF][azure_pdf]

* [SQL Server Mac Install][sql_server_mac]
* [SQL Server Win Install][sql_server_win]

* [OpenWeather API][openweather_api]
* [Nasdaq Time Series][nasdaq_timeseries]
* [Nasdaq Rate Limits][nasdaq_rate_limits]

[azure_pdf]: ./Create_Azure_Free_Account.pdf
[session_5]: ../session_5_ETL_Airflow/README.md

[sql_server_mac]: https://learn.microsoft.com/en-us/sql/azure-data-studio/download-azure-data-studio?view=sql-server-ver16&tabs=redhat-install%2Credhat-uninstall
[sql_server_win]: https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver16

[etl_vs_elt]: https://rivery.io/blog/etl-vs-elt/
[etlt]: https://www.integrate.io/blog/what-is-etlt/
[etl_elt_chart]: https://www.pluralsight.com/resources/blog/cloud/etl-vs-elt-flowchart-when-to-use-each

[openweather_api]: https://home.openweathermap.org/api_keys
[nasdaq_timeseries]: https://docs.data.nasdaq.com/docs/time-series
[nasdaq_rate_limits]: https://docs.data.nasdaq.com/docs/rate-limits
