# Transformations: Azure Synapse Analytics

In previous practice we perform the EL (Extraction, Load) part from the ELT.

In this practice we will focus on the T (Transform) of ELT using Azure as Cloud Data Warehouse and Spark Engine, these services are available as 1 single service in Azure called "Synapse"

![img](documentation_images/synapse_key_capabilities.png)

## What you will learn

* Synapse ELT pipeline
* Synapse Analytics workspace and capabilities
* How to LOAD data from a python script (API + Spark dataframe) into a DB
* How to TRANSFORM data using SQL
* Add permission/role for Synapse in ADF

## Practice

This practice is composed of two parts:

1. EXTRACT and STAGE data from the OpenWeather API with a python script and Spark engine into a csv file
2. LOAD and TRANSFORM the raw data using SQL in the DW

>There are many ways to achieve the same result. For example, the transformation could be done entirely with python and the Spark pool. But for the purpose of this module (ELT) we will execute it as stated above.

Because of time limitations, we will trigger this pipeline manually from Synapse. We could use ADF as orchestrator and make a call to the Synapse pipeline. But, as the scope of the module is ELT, not Azure Cloud, we will focus on the main concepts learned. As optional/advanced feature, you will learn how to connect Synapse and ADF so they can communicate with each other. From that point on, it is for you to explore at your personal convenience. Synapse also has integration capabilities, letting you create and execute pipelines within synapse. It will depend on your business needs what to use and when.

### Step 1 - Dedicated SQL pool

* On your Synapse workspace, go to **Manage** on the left panel, then select **SQL pools** and create a new pool
* Set a name for your DW, select the minimum **Performance level** (DW100C) and **Create**
* Under **Manage > SQL pools** you will see your new pool
  
 ![img](documentation_images/sql_dedicated_and_serverless.png)

>Your dedicated sql pool will generate cost, even if no transactions are going on. If you select your dedicated pool, there is an option to **Pause** it so you keep cost at minimum while not using it. For the duration of this session, you can leave it running and it will cost you just a few dollars, but if you prefer, you can pause it until we arrive to the execution of the SQL script below.

### Step 2- SQL pool in SMSS or Data Studio

* On your Synapse workspace, go to **Manage --> SQL pools** on the left panel, then select your pool
* Copy your workspace endpoint
  
  ![img](documentation_images/sql_pool_endpoint.png)
* Go to SMSS or Data Studio and create a new connection
* In **Server**, paste the workspace endpoint
* Use the username and password you set up while creating the Azure workspace resource
* Right click this connection and create a new query. You will need this statements further down

  ```sql
  SELECT * FROM Weather_london_landing;
  SELECT * FROM Weather_london;

  -- Troubleshooting
  DROP TABLE Weather_london_landing;
  DROP TABLE Weather_london;
  ```

### Step 3 - Python notebook

* On Synapse Studio, on the left panel go to **Develop** tab and **... --> Import** the notebook from this repo
  
  ![img](documentation_images/synapse_import_notebook.png)
* You will need to customize the code with your API key and the path to your datalake container
* API key:
  
  ![img](documentation_images/notebook_api_key.png)
* Datalake path:
  
 ![img](documentation_images/notebook_dl_url.png)
  
>At the bottom of your notebook you will find commented SQL code. Synapse lets you execute different language code using the magic command %%*language*. If we executed this sql code, it will run on the Synapse built-in serverless sql pool and it has some limitations and would throw errors. This is just an overview of the synapse capabilities and of the principles of ELT, in this case, loading data into a landing table in your destination resource, execute your transformation in the DW with SQL and inserting the processed data in a final table.

* Once your code is customized, you need to attach your python notebook with the spark pool you created
  
  ![img](documentation_images/notebook_attatch_spark.png)
* Run cells one by one. For the first one, it may take a few minutes to initialize the spark session.
* Your pd_forecast.csv file in your datalake container should look similar to this
  
  ![img](documentation_images/pd_forecast_preview.png)
* Now you can go on creating your SQL script

### Step 4 - SQL script

* On Synapse Studio, on the left panel go to **Develop** tab and **... --> Import** the sql script from this repo
* You will need to customize the code with url to your datalake container
* Datalake URL:

  ![img](documentation_images/sql_dl_url.png)
* Connect your script to your dedicated sql pool
  
  ![img](documentation_images/sql_script_connect_to_pool.png)
* Run each segment separately for better troubleshooting
* If you can view your processed data in "Weather_london" table...

CONGRATULATIONS! You have successfully run a complete ELT pipeline!

### Optional: ADF - Synapse pipeline

#### Access Control: Role for ADF

* As a general rule, each service that wants to interact with other services should be asigned a role for that purpose.
* On your Synapse workspace, go to **Manage** on the left panel
* Select **Access control** and click **+ Add**
  
  ![img](documentation_images/Synapse_access_control_ADF.png)
* Select the role **Synapse Contributor**
* User: type and select the resource name of your ADF workspace ("data101-abc-df")

#### ADF - Synapse pipeline

* You can go now to ADF, create a pipeline, drag a Notebook activity
* Activity configurations: Synapse artifacts > create new as linked service. Select your synapse notebook, set the spark configurations (ADF, as orchestrator, can launch your spark pool with the same or different configurations)
* Trigger your pipeline. This will only run the python part of this session.
* For running the sql transformations as well to complete the ELT pipeline, you can concatenate two Script activities. One should be for the DDL statements, and the other for the transformations
  
 ![img](documentation_images/ADF_Synapse_pipeline.png)

## Note

Azure Synapse pools have a higher cost, and since you are working on a free account with 200USD, it is recommended that you create the following resources execute the transformations of this practice, and then delete the SQL pool and Spark pool, so you keep the cost at the minimum. Your published scripts or pipelines and the synapse workspace alone will not generate any cost.

## Still curious

In today's lesson we mention cost, cost is probably one of the top 5 factors to consider when using any service and is probably the least considered factor on previous lessons.

Here are some articles about cloud pricing:

* [Breaking the bank on Azure: what Apache Spark tool is the most cost-effective?][azure_costs]
* [Cloud Pricing Comparison: AWS vs. Azure vs. Google Cloud Platform in 2023][comparison_1]
* [Cloud Pricing Comparison 2023: AWS vs Azure vs Google Cloud][comparison_2]
* [AWS, Azure and GCP Service Comparison for Data Science & AI][comparison_data]

We need to be careful, consider:

* What services we use?
* What services we may use?
* Which cloud offers best price?
* Which cloud suits best our needs?
* Learning curve and documentation
* Customer Service and Tecnical Support

## Links

[azure_costs]: https://intercept.cloud/en/news/data-costs-en/
[comparison_1]: https://cast.ai/blog/cloud-pricing-comparison-aws-vs-azure-vs-google-cloud-platform/
[comparison_2]: https://www.simform.com/blog/compute-pricing-comparison-aws-azure-googlecloud/
[comparison_data]: https://www.datacamp.com/cheat-sheet/aws-azure-and-gcp-service-comparison-for-data-science-and-ai
