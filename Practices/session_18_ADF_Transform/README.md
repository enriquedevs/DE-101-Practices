# ADF Transformations

### Prerequisites
* One hour before: Go to your Synapse workspace and create a new spark pool. It takes aproximatle 40 min to provision. Here are the [steps](#spark-pool).

&nbsp; 

### What you will learn
* How to LOAD data from a python script (API + Spark dataframe) into a DB
* Add permission/role for Synapse in ADF

&nbsp; 


# Practice
In this practice we will create some transormations that will be executed leveraging the compute power of a cloud Data Warehouse

&nbsp; 

## Data Flow transformations with ADF

&nbsp; 

## Azure Synapse (Spark, SQL, Python)

The following resources are meant to build a pipeline in ADF that executes a python script from an Azure Synapse notebook running a spark job. The script intends to get data as a dataframe from an API. Then a Copy activity in ADF takes that data and copies it into a database or data warehouse. 

Azure Synapse has a higher cost, and since you are working on a free account with 200USD, it is recommended that you create the following resources execute the transformations of this practice, and then delete the synapse resource (including the SQL and Spark pools), so you keep the cost at the minimum.

* Synapse Workspace
* Synapse Spark pool
* Python notebook
* ADF Synapse linked service (artifact)
* ADF pipeline python to csv

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


## Optional: Create an ADF pipeline to run the python notebook created above


&nbsp; 


#### **Spark pool**


* On your Synapse workspace, go to **Manage** on the left panel, then select **Apache Spark pools** and create a new pool
![img]()
&nbsp; 

    ![img]()
* Wait for 40 minutes aproximately for the pool to be provisioned
* Once successfully provisioned, under **Manage -> Apache Spark pools** click on **Packages**
![img]()
* Upload your "requirements.txt" file. This may take up to 20 minutes.


&nbsp; 

**ADF pipeline**

* Go to your ADF workspace
* Create a new pipeline, set a propper name
* Drag a new **Notebook** activity under **Synapse**
* Go to **Azure Synapse Analytics (Artifacts)** in the activity configurations and create a new linked service:
![img](documentation_images/ADF_synapse_artifact_ls.png)
* Fill in the values as follow:
![img](documentation_images/synapse_linked_service.png)
* Under **Settings** in your activity configurations, set the spark pool configs the same as the one you created in your Synapse workspace
![img](documentation_images/ADF_spark_settings.png)
* Drag a new **Copy** activity and connect the notebook to the copy activity
![img](documentation_images/ADF_connect_notebook_copy_activity.png)

... steps under construction ...

* On the **Sink** tab in your activity configurations, create a new dataset, select "Azure SQL Database", select the proper linked service, database and table ("AAPL_synapse")
* You can import the schema, or import it later under **Mapping** tab
* Click **Validate** and if there are no errors, click on **Publish** and then **Debug** or **Trigger now**
* Go to Data Studio or SSMS, run a SELECT query to view the data
* Once the data is in place in the database
