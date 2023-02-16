# Practice: batch data pipeline with Airflow, HDFS, Hive and Spark

In this practice you will implement a data pipeline using a batch architecture. Notice that the arquitecture used here is not a lambda architecture, because we will leave the streaming part for another –more advanced– course.

## What you will do

- Use HDFS as a data lake
- Use Hive to query data in HDFS
- Issue processing jobs in Spark
- Use Hive as a data warehouse
- Configure connections to external services in Airflow
- Use Airflow to orchestrate the data pipeline

## Pre-requisites

- Install Docker
- Install Docker Compose

## Setup

### Build and start the environment

Start up the docker containers by running the following command in the current directory. If you cannot run the shell script, you can run the commands in the script manually, one by one. Notice that the first time you run this command it will take up to 30 minutes to download and build the images.

```bash
./start.sh
```

Now, run the following command to check that the containers are running. Make sure that all the containers are in the `healthy` state. If that is not the case, run the `stop.sh` script and and then the `start.sh` script again.

```bash
docker ps
```

If all the containers are in the `healthy` state, open the Airflow UI by going to <http://localhost:8080>. The default username and password are `airflow`.

## The practice

While the code of the DAG is already available under `mnt/airflow/dags/forex_data_pipeline.py`, in this practice we will focus on creating and testing the connections and resources that support the data pipeline, in order to highlight the infrastructure of this batch job, that will use a data lake, a data warehouse, a processing engine and an orchestrator to coordinate the ELT and ETL processes involved in the data pipeline.

As an overview of the data pipeline, we will:

1. Verify that the URL that points to the JSON data that holds the forex rates is reachable.
2. Verify that the local file where we will store the data is available.
3. Download the data from the URL and store it in the local file.
4. Load the data from the local file into HDFS.
5. Submit a Spark job, process the data from HDFS and store the results in a Hive table.
6. Send a notification via Slack.

### 0. The architecture

The software architecture that underlies the data pipeline is the following:
![architecture](docs/architecture.png)

- [HDFS](https://aws.amazon.com/es/emr/details/hadoop/what-is-hadoop/) is the data lake where we will store the data.
- [Hive](https://aws.amazon.com/es/big-data/what-is-hive/) will make the data in HDFS available for querying.
- [Spark](https://aws.amazon.com/es/big-data/what-is-spark/) is a distributed processing engine that will run the processing job.
- [Hue](https://gethue.com/) is a web interface for data warehousing and analytics. It will allow us to query the data in HDFS and Hive.
- [Postgres](https://www.postgresql.org/) is a relational database management system that will work as Hive's metastore.
- [Adminer](https://www.adminer.org/) is a web interface for Postgres and other databases that we don't need to use in this practice.

### 1. Check if the URL is reachable – `HttpSensor`

The first task in the DAG is an [`HttpSensor`](https://airflow.apache.org/docs/apache-airflow-providers-http/stable/_api/airflow/providers/http/sensors/http/index.html#airflow.providers.http.sensors.http.HttpSensor) that will check if the URL that points to the JSON data that holds the forex rates is reachable.

For this task to work we will need to create a connection to the URL that we specify in the `HttpSensor` operator. To do so, go to the Airflow UI and click on the `Admin` tab. Then, click on the `Connections` link. Click on the `+` button to add a new record and fill the form with the following values:

- Conn Id: `forex_api`
- Conn Type: `HTTP`
- Host: <https://gist.github.com>

Click on the `Save` button to save the connection.

In order to test that the task works, first run the following command to open a shell in the Airflow container:

```bash
docker exec -it airflow /bin/bash
```

Now, run the following command to run the task. The last argument is an execution date in the past. This is required by Airflow to determine if the task should be executed.

```bash
airflow tasks test forex_data_pipeline is_forex_rates_available 2023-02-12
```

If everything is correct, then we should get a message like the following right before the end of the logs:

```bash
[2023-02-14 02:20:03,835] {base.py:248} INFO - Success criteria met. Exiting.
```

### 2. Check if the currency file is available – `FileSensor`

The following task is a [`FileSensor`](https://airflow.apache.org/docs/apache-airflow-providers-http/stable/_api/airflow/providers/http/sensors/http/index.html#airflow.providers.http.sensors.http.HttpSensor) that will check if the local file where we will store the data exists.

For this task we will create a connection to the local file system. To do so, go to the Airflow UI and click on the `Admin` tab. Then, click on the `Connections` link. Click on the `+` button to add a new record and fill the form with the following values:

- Conn Id: `forex_path`
- Conn Type: `File (path)`
- Extra: `{"path": "/opt/airflow/dags/files"}`

Click on the `Save` button to save the connection.

Just like in the previous task, we will test the task by running the following command in the Airflow container:

```bash
airflow tasks test forex_data_pipeline is_forex_currencies_file_available 2023-02-12
```

### 3. Download the data from the URL – `PythonOperator`

The next task is a [`PythonOperator`](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/python/index.html#airflow.operators.python.PythonOperator) that will download the data from the `BASE_URL` inside the `download_rates` function and store it in the local file.

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

```bash
airflow tasks test forex_data_pipeline download_rates 2023-02-12
```

### 4. Save forex rates into HDFS – `BashOperator`

The next task is a [`BashOperator`](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/bash/index.html#airflow.operators.bash.BashOperator) that will load the data from the local file into HDFS.

The `BashOperator` executes a couple of bash commands. The first one is a `hdfs dfs` command that will create the directory where we will store the data. The second one is a `hdfs dfs` command that will copy the data from the local file to HDFS.

Before testing the operator, go to the Hue UI by accessing the following URL: <http://localhost:32762>. The username we will use is `root` and the password is `root`. Click on `Create Account`, then after waiting close the tutorial. Afterwards, click on the hamburger menu on the top left corner and click on `Files`. You will land by default in `/user/root`. You can click on `/` to go to the root directory of HDFS. This is a view of the HDFS file system and here we will see any updates to HDFS.

Now, in order to test the task, we will run the following command in the Airflow container:

```bash
airflow tasks test forex_data_pipeline save_rates_to_hdfs 2023-02-12
```

By refreshing the Hue UI, we should see the directory `/forex_rates` in the root directory of HDFS.

### 5. Create a Hive table – `HiveOperator`

For the following task we will use the [`HiveOperator`](https://airflow.apache.org/docs/apache-airflow/1.10.10/_api/airflow/operators/hive_operator/index.html#airflow.operators.hive_operator.HiveOperator). We will use this operator to create a Hive table that will store the data from HDFS.

In order for this connection to work we first need to create the connection (`hive_conn`) that we have specified in the `hive_cli_conn_id` parameter. To do so, go to the Airflow UI and click on the `Admin` tab. Then, click on the `Connections` link. Click on the `+` button to add a new record and fill the form with the following values:

- Conn Id: `hive_conn`
- Conn Type: `Hive Server 2 Thrift`
- Host: `hive-server`
- Login: `hive`
- Password: `hive`
- Port: `10000`

Now, before testing the operator, go back to the Hue UI and click on the `Tables` menu on the left. The UI should show that there are no tables in the `default` database. This is because we have not created any tables yet.

Now, run the following command in the Airflow container to test the task:

```bash
airflow tasks test forex_data_pipeline creating_forex_rates_table 2023-02-12
```

If you go back to the Hue UI and click on the `Refresh` button on the upper right corner, you should now see that the `forex_rates` table has been created.

One thing that you can do to test the table is to click in the `forex_rates` table entry and then click on the `▶️ Query` button, which will automatically execute the following query:

```sql
SELECT * FROM `default`.`forex_rates` LIMIT 100;
```

This query will return no results because we have not loaded any data into the table yet. We will do that in the next task.

### 6. Process the forex rates with Spark – `SparkSubmitOperator`

The next task is a [`SparkSubmitOperator`](https://airflow.apache.org/docs/apache-airflow/1.10.12/_api/airflow/contrib/operators/spark_submit_operator/index.html#airflow.contrib.operators.spark_submit_operator.SparkSubmitOperator) that will process the data from HDFS and store the results in a new table.

The `SparkSubmitOperator` will execute the `mnt/airflow/dags/scripts/forex_processing.py` script. The script will read the data from the `forex_rates` table and process it. You don't really need to understand the details of the Spark job, but in order to give you a correct mental model of what is happening in this task, the processing consists of the following steps:

1. The Spark job will create a SparkSession. This object is the entry point to Spark and contains the information about the Spark application.
2. We will use the SparkSession to read the data from HDFS at <hdfs://namenode:9000/forex/forex_rates.json>. The resulting object is a Spark DataFrame –pretty similar in concept to a Pandas DataFrame, although the Spark DataFrames are distributed in nature and every operation performed on them is lazy–.
3. We will select several variables from the resulting DataFrame, drop duplicates and fill missing values with '0'. These operations do not ocur in place, so we are virtually creating a new DataFrame.
4. Finally we will append the resulting DataFrame to the `forex_rates` Hive table.

As before, for this task to work we need to create the connection (`spark_conn`) that we have specified in the `conn_id` parameter. To do so, go to the Airflow UI and click on the `Admin` tab. Then, click on the `Connections` link. Click on the `+` button to add a new record and fill the form with the following values:

- Conn Id: `spark_conn`
- Conn Type: `Spark`
- Host: `spark://spark-master`
- Port: `7077`

With this, we are ready to test the task, so run the following command in the Airflow container:

```bash
airflow tasks test forex_data_pipeline forex_processing 2023-02-12
```

If you go back to the Hue UI and run the same query as before, you should now see that the table has been updated with the processed data as expected.

Furthermore, if you want to see how the data is stored in Hive, you can click on the `Files` menu on the left and go to the `/user/hive/warehouse/forex_rates` directory. You will see that the data is stored in raw format.

### 7. Send a notification via Slack – `SlackWebhookOperator`

If time allows, we will also add a task that will send a notification to a Slack channel. This task will use the [`SlackWebhookOperator`](https://airflow.apache.org/docs/apache-airflow/1.10.12/_api/airflow/contrib/operators/slack_webhook_operator/index.html#airflow.contrib.operators.slack_webhook_operator.SlackWebhookOperator).

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

```bash
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
```

Now, we need to create the connection (`slack_conn`) that we have specified in the `http_conn_id` parameter. To do so, once again go to the Airflow UI and click on the `Admin` tab. Then, click on the `Connections` link. Click on the `+` button to add a new record and fill the form with the following values:

- Conn Id: `slack_conn`
- Conn Type: `HTTP`
- Host: `<https://hooks.slack.com/services/>
- Password: `T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX` (the part of the webhook URL that contains the token)

In order test the task, please run the following command in the Airflow container:

```bash
airflow tasks test forex_data_pipeline send_slack_notification 2023-02-12
```

If everything went well, you should see a notification in the Slack channel you created before.

### 8. Run the DAG

Go back to the Airflow UI and enable the DAG by clicking on the toggle button on the left. After refreshing a couple of times, you should see the DAG run in the UI.

You can also click on the DAG name to see the details of the run and also click on the "Graph View" tab to see the DAG visualized as a graph.

If everything went well, then congratulations! You have successfully configured and executed a complete data pipeline with Airflow.

### Cleanup

To stop the Spark cluster, run the following command:

```bash
./stop.sh
```
