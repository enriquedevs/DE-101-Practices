# ELT Environments and Database Integration Tools

In this practice we will setup the environment, tools and resources necesary for the following sessions.


### Prerequisites
* Azure Free Account ([Instructions](Create_Azure_Free_Account.pdf))
* Azure Data Studio or SQL Server Management Studio ([Data Studio](https://learn.microsoft.com/en-us/sql/azure-data-studio/download-azure-data-studio?view=sql-server-ver16&tabs=redhat-install%2Credhat-uninstall), [SSMS](https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver16))
* SQL Server for macos with Docker (optional) ([docker-compose.yml](docker-compose.yml))
* Nasdaq Free Account ([Create Nasdaq Account](https://data.nasdaq.com/account/profile))
* Nasdaq api key file ([API under Account Settings](https://data.nasdaq.com/account/profile)):
```
    touch .nasdaqapikey
```
Open it with a text editor and paste your api key. Save it to your documents or anywhere else.

&nbsp; 

### What you will learn
* How to create resources on Azure Portal
* How to connect to a Database in Azure with Data Studio or SSMS
* ADF linked services (Http, Database, Datalake, Synapse DW and notebook)
* (Advanced / optional) How to create a Data Warehouse in Azure Synapse (runs sql dw (olap) and spark with "massively parallel programming" under the hood)
* (Advanced / optional) How to get data with a python script in Synapse

&nbsp; 

&nbsp; 

# Practice

You are a data engineer working for a credit rating agency. You need to get Stock Market Data every day, store it in a Data Warehouse for financial research and analysis for further publication. You work in the team responsible of getting data from the Nasdaq Index from different resources or formats.

&nbsp; 

&nbsp; 

# STEP 1


**Resource Group**

* In your Azure portal, type in and select "Resource groups"
![img](documentation_images/resource_group.png)

* Select **+ Create** and follow the instructions. Name suggested similar to "data-eng-101-rg"
* Region: remember that all your resources should be in the same region. In this course, for those in Mexico, South Central US is recommended. Leave the rest with the defaults. Go to **Review + create** and click **Create**.

&nbsp; 

**Blob Storage**

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
* Then go to the created container and click **Upload** from the tabs section and upload the files from this data folder in this session (git repo)

Go to blob account and create container and data folder. Upload csv file

&nbsp; 

**Data Lake Storage**

+ Redo steps from **Blob Storage**  
+ After choosing Redundancy, go to **Advanced** tab and in the **Data Lake Storage Gen 2** section, check the box **Enable hierarchical namespace**  
+ Leave the rest with the defaults and **Create**  
+ Go to **All Resources** in your Azure portal and select this storage account 
+ Create three containers, "raw", "processed", "data101_synapse"

&nbsp; 

**SQL Server**

* Type in and select "SQL servers"
* Select **+ Create** and follow the instructions
* Set a server name. Suggested similar to "data101-srv-abc"
* Select the same region as your resource group
* Authentication: seletc **SQL Authentication** and set an admin username and strong password (remember or write down this info for further use)
* Networking: Select **YES** for **Allow Azure services and resources to access this server**
* Leave the rest with defaults and **Create**

&nbsp; 

**SQL Database**

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

&nbsp; 

**Dedicated SQL Pool**

* Type in and select "SQL servers"
* Select **+ New dedicated SQL pool (formerly SQL DW)**
* Name: "AdventureWorksDW"
* Performance level: **DW100c**
* Additional settings tab --> Data source: Sample
* Leave the rest with the defaults and **Create**
* Refresh the connection in SSMS or Data Studio and you should see this DW listed

&nbsp; 

**Azure Data Factory (Workspace)**

* Type in and select **Data factories**
* Select **+ Create**
* Select **Resource group** and **Region** the same as all the above
* Set any name. Suggested similar to "data101-abc-df"
* Leave the defaults and **Create**
* Go to **All Resources**, select this data factory and click on **Launch Studio**
* It will open a new page like this:
![img](documentation_images/ADF_home.png)

&nbsp; 

&nbsp; 

# STEP 2


**Azure Data Factory (Linked Services)**

* **HTTP**
  * On your ADF workspace, on the left panel select **Manage**, click on **Linked services** and create a new one
  * On the search bar, type in and select **HTTP** and set the following values:
![img](documentation_images/http_ls.png)
  * Test connection and create
  * Note: for other REST APIs, you can configure the authentication type along with specific authentication headers

&nbsp; 

* **Azure Blob Storage**
  * On your ADF workspace, on the left panel select **Manage**, click on **Linked services** and create a new one
  * On the search bar, type in and select **Azure Blob Storage** and set the following values:
  ![img](documentation_images/blob_ls.png)
  * Test connection and create

&nbsp; 

* **Azure Data Lake Storage Gen2**
  * Redo the steps above but type in and select **Azure Data Lake Storage Gen2**, then fill in the corresponding values

&nbsp; 

* **Azure SQL Database**
  * On your ADF workspace, on the left panel select **Manage**, click on **Linked services** and create a new one
  * On the search bar, type in and select **Azure SQL Database**, then fill in the corresponding values

&nbsp; 

* **Azure Dedicated SQL pool**
  * On your ADF workspace, on the left panel select **Manage**, click on **Linked services** and create a new one
  * On the search bar, type in and select **Azure Synapse Analytics**
  * Name: "adventureworks_dw_ls"
  * On Server name drop down list, select the "yourservername(SQL server)" option
  * Then select Database name: "AdventureWorksDW"
  * Enter the username and password of your Azure SQL server, test connection and create

&nbsp; 

&nbsp; 

# STEP 3 (Advanced / optional) 

* **Snowflake linked service**
  * On your ADF workspace, on the left panel select **Manage**, click on **Linked services** and create a new one
  * On the search bar, type in and select **Snowflake**
  * Name: "snowflake_ls"
  * Enter your snowflake account ("accountname.southcentral-us.azure")
  * Fill in the values for user, pssw, db, dw and role
  * Test your connection and create
  ![img](documentation_images/ADF_snowflake_ls.png)

&nbsp; 

## Azure Synapse Analytics

The following resources are meant to build a pipeline in ADF that executes a python script from an Azure Synapse notebook running a spark job. The script intends to get data as a dataframe from an API. Then a Copy activity in ADF takes that data and copies it into a database or data warehouse. 

Azure Synapse has a higher cost, and since you are working on a free account with 200USD, it is recommended that you create the following resources and build your pipeline on the third session of this module. Once you finished and executed your pipeline, delete the synapse resource (including the SQL and Spark pools), so you keep the cost at the minimum.

* Synapse Workspace
* Synapse Access Control
* Synapse Spark pool
* Python notebook
* ADF Synapse linked service (artifact)
* ADF pipeline python to DB

To mantain the structure of the sessions, here you will find the instructions to setup the resources and configurations necessary for the copy activity. You can find the **Copy** activity at the bottom of practice #17. But remember, once again, that it is recommended to follow this steps after the session #18 and in the same day, to keep cost at the minimum.

**Azure Synapse(Workspace)**

* Type in and select **Azure Synapse Analytics**
* Select **+ Create**
* Select **Resource group** and **Region** the same as all the above (Leave **Managed resource group** blank)
* Set any name. Suggested similar to "data101-synapse-abc"
* Account name: select the datalake resource created above
* File system name: select "data101_synapse"
* Under security tab, set a new SQL admin user and password (this is a different logical server than the created above)
* Leave the defaults and **Create**
* Go to **All Resources**, select this synapse resource and click on **Launch Studio**
* It will open a new page similar to ADF workspace
* Note: Synapse Studio does not load on Safari

**Synapse Access Control / Role for ADF**

* First of all we need to asign ADF a proper role to interact with Synapse. As a general rule, each service that wants to interact with other services should be asigned a role for that purpose. 
* On your Synapse workspace, go to **Manage** on the left panel
* Select **Access control** and click **+ Add**
  ![img](documentation_images/Synapse_access_control_ADF.png)
* Select the role **Synapse Contributor**
* User: type and select the resource name of your ADF workspace ("data101-abc-df")

&nbsp; 
