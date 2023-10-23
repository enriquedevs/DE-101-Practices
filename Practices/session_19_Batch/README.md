# Batch data pipeline with Airflow, HDFS, Hive and Spark

In this practice you will implement a data pipeline using a batch architecture.

>Notice that the arquitecture used here is not a lambda architecture, because we will leave the streaming part for another –more advanced– course.

## What you will do

* Use HDFS as a data lake
* Use Hive to query data in HDFS
* Issue processing jobs in Spark
* Use Hive as a data warehouse
* Configure connections to external services in Airflow
* Use Airflow to orchestrate the data pipeline

## Practice

While the code of the DAG is already available under `mnt/airflow/dags/forex_data_pipeline.py`, in this practice we will focus on creating and testing the connections and resources that support the data pipeline, in order to highlight the infrastructure of this batch job, that will use a data lake, a data warehouse, a processing engine and an orchestrator to coordinate the ELT and ETL processes involved in the data pipeline.

As an overview of the data pipeline, we will:

1. Verify that the URL that points to the JSON data that holds the forex rates is reachable.
2. Verify that the local file where we will store the data is available.
3. Download the data from the URL and store it in the local file.
4. Load the data from the local file into HDFS.
5. Submit a Spark job, process the data from HDFS and store the results in a Hive table.
6. Send a notification via Slack.

### Architecture

The software architecture that underlies the data pipeline is the following:

* [HDFS][hdfs] is the data lake where we will store the data.
* [Hive][hive] will make the data in HDFS available for querying.
* [Spark][spark] is a distributed processing engine that will run the processing job.
* [Hue][hue] is a web interface for data warehousing and analytics. It will allow us to query the data in HDFS and Hive.
* [PostgreSQL][postgresql] is a relational database management system that will work as Hive's metastore.
* [Adminer][adminer] is a web interface for Postgres and other databases that we don't need to use in this practice.

  ![architecture](docs/architecture.png)

### Step 0 - Start the environment

Start up the docker containers by running the following command in the current directory.

```sh
./start.sh
```

Now, run the following command to check that the containers are running. Make sure that all the containers are in the `healthy` state.

```sh
docker ps
```

If all the containers are in the `healthy` state, open the Airflow UI by going to <http://localhost:8080>. The default username and password are `airflow`.

### Step 1 - Check if the URL is reachable (HttpSensor)

The first task in the DAG is an [HttpSensor][http_sensor] that will check if the URL that points to the JSON data that holds the forex rates is reachable.

For this task to work we will need to create a connection to the URL that we specify in the `HttpSensor` operator. To do so, go to the Airflow UI and click on the `Admin` tab. Then, click on the `Connections` link. Click on the `+` button to add a new record and fill the form with the following values:

* Conn Id: `forex_api`
* Conn Type: `HTTP`
* Host: <https://gist.github.com>

Click on the `Save` button to save the connection.

In order to test that the task works, first run the following command to open a shell in the Airflow container:

```sh
docker exec -it airflow /bin/bash
```

Now, run the following command to run the task. The last argument is an execution date in the past. This is required by Airflow to determine if the task should be executed.

```sh
airflow tasks test forex_data_pipeline is_forex_rates_available 2023-02-12
```

If everything is correct, then we should get a message like the following right before the end of the logs:

```log
[2023-02-14 02:20:03,835] {base.py:248} INFO - Success criteria met. Exiting.
```

### Step 2 - Check if the currency file is available (FileSensor)

The following task is a [FileSensor][file_sensor] that will check if the local file where we will store the data exists.

For this task we will create a connection to the local file system. To do so, go to the Airflow UI and click on the `Admin` tab. Then, click on the `Connections` link. Click on the `+` button to add a new record and fill the form with the following values:

* Conn Id: `forex_path`
* Conn Type: `File (path)`
* Extra: `{"path": "/opt/airflow/dags/files"}`

Click on the `Save` button to save the connection.

Just like in the previous task, we will test the task by running the following command in the Airflow container:

```bash
airflow tasks test forex_data_pipeline is_forex_currencies_file_available 2023-02-12
```

### Step 3 - Download the data from the URL (PythonOperator)

The next task is a [PythonOperator][python_operator] that will download the data from the `BASE_URL` inside the `download_rates` function and store it in the local file.

Although the details of the `download_rates` function are not important for this practice, we will briefly explain what it does. The function will download every possible pair of currencies present in the `forex_currencies.csv` file and store the data in the `forex_rates.json` file. The data will be stored in the following format:

```json
[
    {
        "base": "EUR", 
        "rates": {
            "USD": 1.13, "NZD": 1.41, "JPY": 101.89, "GBP": 0.36, "CAD": 1.21
        }, 
        "last_update": "2021-01-01"
    }
]
```

In order to test the task, we will run the following command in the Airflow container:

```sh
airflow tasks test forex_data_pipeline download_rates 2023-02-12
```

### Step 4 - Save forex rates into HDFS (BashOperator)

The next task is a [BashOperator][bash_operator] that will load the data from the local file into HDFS.

The `BashOperator` executes a couple of bash commands. The first one is a `hdfs dfs` command that will create the directory where we will store the data. The second one is a `hdfs dfs` command that will copy the data from the local file to HDFS.

Before testing the operator, go to the Hue UI by accessing the following URL: <http://localhost:32762>. The username we will use is `root` and the password is `root`. Click on `Create Account`, then after waiting close the tutorial. Afterwards, click on the hamburger menu on the top left corner and click on `Files`. You will land by default in `/user/root`. You can click on `/` to go to the root directory of HDFS. This is a view of the HDFS file system and here we will see any updates to HDFS.

Now, in order to test the task, we will run the following command in the Airflow container:

```sh
airflow tasks test forex_data_pipeline save_rates_to_hdfs 2023-02-12
```

By refreshing the Hue UI, we should see the directory `/forex_rates` in the root directory of HDFS.

### Step 5 - Create a Hive table (HiveOperator)

For the following task we will use the [HiveOperator][hive_operator]. We will use this operator to create a Hive table that will store the data from HDFS.

In order for this connection to work we first need to create the connection (`hive_conn`) that we have specified in the `hive_cli_conn_id` parameter. To do so, go to the Airflow UI and click on the `Admin` tab. Then, click on the `Connections` link. Click on the `+` button to add a new record and fill the form with the following values:

* Conn Id: `hive_conn`
* Conn Type: `Hive Server 2 Thrift`
* Host: `hive-server`
* Login: `hive`
* Password: `hive`
* Port: `10000`

Now, before testing the operator, go back to the Hue UI and click on the `Tables` menu on the left. The UI should show that there are no tables in the `default` database. This is because we have not created any tables yet.

Now, run the following command in the Airflow container to test the task:

```sh
airflow tasks test forex_data_pipeline creating_forex_rates_table 2023-02-12
```

If you go back to the Hue UI and click on the `Refresh` button on the upper right corner, you should now see that the `forex_rates` table has been created.

One thing that you can do to test the table is to click in the `forex_rates` table entry and then click on the `▶️ Query` button, which will automatically execute the following query:

```sql
SELECT * FROM `default`.`forex_rates` LIMIT 100;
```

This query will return no results because we have not loaded any data into the table yet. We will do that in the next task.

### Step 6 - Process the forex rates with Spark (SparkSubmitOperator)

The next task is a [SparkSubmitOperator][spark_submit_operator] that will process the data from HDFS and store the results in a new table.

The `SparkSubmitOperator` will execute the `mnt/airflow/dags/scripts/forex_processing.py` script. The script will read the data from the `forex_rates` table and process it. You don't really need to understand the details of the Spark job, but in order to give you a correct mental model of what is happening in this task, the processing consists of the following steps:

1. The Spark job will create a SparkSession. This object is the entry point to Spark and contains the information about the Spark application.
2. We will use the SparkSession to read the data from HDFS at <hdfs://namenode:9000/forex/forex_rates.json>. The resulting object is a Spark DataFrame –pretty similar in concept to a Pandas DataFrame, although the Spark DataFrames are distributed in nature and every operation performed on them is lazy–.
3. We will select several variables from the resulting DataFrame, drop duplicates and fill missing values with '0'. These operations do not ocur in place, so we are virtually creating a new DataFrame.
4. Finally we will append the resulting DataFrame to the `forex_rates` Hive table.

As before, for this task to work we need to create the connection (`spark_conn`) that we have specified in the `conn_id` parameter. To do so, go to the Airflow UI and click on the `Admin` tab. Then, click on the `Connections` link. Click on the `+` button to add a new record and fill the form with the following values:

* Conn Id: `spark_conn`
* Conn Type: `Spark`
* Host: `spark://spark-master`
* Port: `7077`

With this, we are ready to test the task, so run the following command in the Airflow container:

```sh
airflow tasks test forex_data_pipeline forex_processing 2023-02-12
```

If you go back to the Hue UI and run the same query as before, you should now see that the table has been updated with the processed data as expected.

Furthermore, if you want to see how the data is stored in Hive, you can click on the `Files` menu on the left and go to the `/user/hive/warehouse/forex_rates` directory. You will see that the data is stored in raw format.

### Step 7 - Send a notification via Slack (SlackWebhookOperator)

If time allows, we will also add a task that will send a notification to a Slack channel. This task will use the [SlackWebhookOperator][slack_webhook_operator].

In order for this task to work, we need to create first a Slak workspace. To do so, follow these steps:

1. Go to <http://www.slack.com>.
2. Click on "Create a new workspace".
3. Enter your work email address and click on "Continue".
4. You will receive an email with a code to verify your email address. Enter the code and click on "Continue".
5. Click on "Create a new workspace".
6. Enter the name of the workspace and click on "Next".
7. If you wish, you can add your course partners as collaborators. If that's not the case, you can omit this step.
8. When you're asked "What's your team working on right now?" you can enter the name of the channel you want to create. For example, you can enter "airflow-notifications".

Now that we have created the channel to send the notifications to, we need to create a Slack app. To do so, follow these steps:

1. Go to <https://api.slack.com/apps>.
2. Click on "Create New App".
3. Click on "From scratch".
4. Create a name for the app (like `airflow-notifier`) and select the workspace you created in the previous step.
5. Click on "Create App".
6. Go to the "Add features and functionality" section and click on "Incoming Webhooks".
7. Right besides the "Activate Incoming Webhooks" legend toggle the switch to "On" in order to activate the feature.
8. Scroll to the bottom of the page and click on "Add New Webhook to Workspace".
9. Select the channel you created before (`airflow-notifications`) in the previous step and click on "Allow".
10. Copy the webhook URL that appears in the "Webhook URL for your workspace" section.

Notice that the webhook URL looks like this:

```txt
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
```

Now, we need to create the connection (`slack_conn`) that we have specified in the `http_conn_id` parameter. To do so, once again go to the Airflow UI and click on the `Admin` tab. Then, click on the `Connections` link. Click on the `+` button to add a new record and fill the form with the following values:

* Conn Id: `slack_conn`
* Conn Type: `HTTP`
* Host: <https://hooks.slack.com/services/>
* Password: `T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX` (the part of the webhook URL that contains the token)

In order test the task, please run the following command in the Airflow container:

```sh
airflow tasks test forex_data_pipeline send_slack_notification 2023-02-12
```

If everything went well, you should see a notification in the Slack channel you created before.

### Step 8 - Run the DAG

Go back to the Airflow UI and enable the DAG by clicking on the toggle button on the left. After refreshing a couple of times, you should see the DAG run in the UI.

You can also click on the DAG name to see the details of the run and also click on the "Graph View" tab to see the DAG visualized as a graph.

If everything went well, then congratulations! You have successfully configured and executed a complete data pipeline with Airflow.

### Cleanup

To stop the Spark cluster, run the following command:

```bash
./stop.sh
```

## Still curious

* Airflow is one of the most common technologies for data pipelines, if you want to start creating your own pipelines you need to understand, how to pre-made solutions mounts into your instance.

  Since airflow is build modularly it's quite similar to add libraries to your code, these can be:

  * Providers \
    Providers can contain operators, hooks, sensor, and transfer operators to communicate with a multitude of external systems, but they can also extend Airflow core with new capabilities. \
    [Documentation][provider]
  * Core extensions \
    They can be used to extend core by implementations of Core features, specific to certain providers \
    [Documentation][core_ext]
  * Packages \
    This is the library itself for a provider. \
    Ex. Amazon (Provider) -> apache-airflow-providers-amazon (Package) \
    [Documentation][package]
  * Operators
    An Operator is conceptually a template for a predefined Task, that you can just define declaratively inside your DAG. \
    [Documentation][operator]
  * Hooks \
    A Hook is a high-level interface to an external platform that lets you quickly and easily talk to them without having to write low-level code that hits their API or uses special libraries. They’re also often the building blocks that Operators are built out of. \
    [Documentation][conn_and_hook]
  * Connection \
    A Connection is essentially set of parameters - such as username, password and hostname - along with the type of system that it connects to, and a unique name, called the conn_id. \
  [Documentation][conn_and_hook]

* What if the functionality I need does not exists?

  Let's imagine you have a pipeline that receives sales data, but the data you receive only contains customer id and product id, but you need to fill that data from another system such as a CRM like SAP.

  The good practice of airflow says most of the external system interaction should be made either by a hook or by an operator.

  In this case we can create a custom hook or a custom operator that we can later reuse as many times as we want.

  * How we do it?
    * Article: [Airflow — Writing your own Operators and Hooks][custom_hook_and_operator]

* What are airflow best practices?

  Before considering airflow into our pipeline, we need to understand what airflow is for:
  > Airflow is an orchestrator with coding capabilities

  This means, despite the fact airflow can run python and some other code scripts, it does not have the same memory or processing power as a dedicated server.

  * So this means `PythonOperator` is useless?

    No, this means we should not rely 100% in operators to do all the transforming steps, we should optimize memory to trigger tasks in a more powerful environment, then return with the operation results.

  Article: [Airflow Best Practices][airflow_best_practices]

## Links

* [HDFS][hdfs]
* [Hive][hive]
* [Spark][spark]
* [Hue][hue]
* [Postgres][postgresql]
* [Adminer][adminer]
* [HTTP Sensor][http_sensor]
* [File Sensor][file_sensor]
* [Python Operator][python_operator]
* [Bash Operator][bash_operator]
* [HiveOperator][hive_operator]
* [SparkSubmitOperator][spark_submit_operator]
* [SlackWebhookOperator][slack_webhook_operator]
* [Airflow — Writing your own Operators and Hooks][custom_hook_and_operator]
* [Airflow Best Practices][airflow_best_practices]

[hdfs]: https://aws.amazon.com/es/emr/details/hadoop/what-is-hadoop/
[hive]: https://aws.amazon.com/es/big-data/what-is-hive/
[spark]: https://aws.amazon.com/es/big-data/what-is-spark/
[hue]: https://gethue.com/
[postgresql]: https://www.postgresql.org/
[adminer]: https://www.adminer.org/
[http_sensor]: https://airflow.apache.org/docs/apache-airflow-providers-http/stable/_api/airflow/providers/http/sensors/http/index.html#airflow.providers.http.sensors.http.HttpSensor
[file_sensor]: https://airflow.apache.org/docs/apache-airflow-providers-http/stable/_api/airflow/providers/http/sensors/http/index.html#airflow.providers.http.sensors.http.HttpSensor
[python_operator]: https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/python/index.html#airflow.operators.python.PythonOperator
[bash_operator]: https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/bash/index.html#airflow.operators.bash.BashOperator
[hive_operator]: https://airflow.apache.org/docs/apache-airflow/1.10.10/_api/airflow/operators/hive_operator/index.html#airflow.operators.hive_operator.HiveOperator
[spark_submit_operator]: https://airflow.apache.org/docs/apache-airflow/1.10.12/_api/airflow/contrib/operators/spark_submit_operator/index.html#airflow.contrib.operators.spark_submit_operator.SparkSubmitOperator
[slack_webhook_operator]: https://airflow.apache.org/docs/apache-airflow/1.10.12/_api/airflow/contrib/operators/slack_webhook_operator/index.html#airflow.contrib.operators.slack_webhook_operator.SlackWebhookOperator

[provider]: https://airflow.apache.org/docs/apache-airflow-providers/
[core_ext]: https://airflow.apache.org/docs/apache-airflow-providers/core-extensions/index.html
[package]: https://airflow.apache.org/docs/apache-airflow-providers/packages-ref.html
[operator]: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/operators.html
[conn_and_hook]: https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/connections.html

[custom_hook_and_operator]: https://medium.com/b6-engineering/airflow-writing-your-own-operators-and-hooks-93fcfbc7bd
[airflow_best_practices]: https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html
