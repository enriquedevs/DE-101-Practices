# ETL Introduction and Airflow

In this practice we will develop a simple ETL pipeline on Airflow to understand each part of the ETL process

![Docker-Python](documentation_images/etl-3.jpg)

## Prerequisites

* Follow the [pre-setup guideline][pre-setup]

## Before start

Let's review some concepts and technologies we used during the pre-setup:

### ETL

>ETL stands for `Extract, Transform, Load`, and it refers to the process of extracting data from one or more sources, transforming the data into a suitable format, and loading it into a target destination for storage or analysis.

* `Extract` \
  Data is extracted from one or more sources (databases, files, APIs...) \
  It may be necessary to perform some data cleaning or filtering to ensure that only the relevant data is extracted.
* `Transform` \
  Extracted data is transformed into a suitable format for analysis or storage. \
  This may involve cleaning the data, reformatting it, combining it with other data sources, or performing other data transformations.
* `Load` \
  Transformed data is loaded into a target destination.(database, a data warehouse, a data lake...)

>Once the data is loaded it can be used for reporting, querying...

![img](documentation_images/etl-2.png)

>For ETL, there are many platforms, tools and frameworks that can be used to implement an ETL Pipeline, such as: `NiFi`, `Airflow`, `AWS Data Pipeline`, `Azure Data Factory`...

### Airflow

>`Airflow` is an open-source platform that is an `Orchestrator` to manage `pipelines` (usually data pipelines) on `Python Code`.

Here are some important concepts to understand about Airflow:

* `DAG` \
  A DAG (Directed Acyclic Graph) is the core concept of Airflow, collecting Tasks together, organized with dependencies and relationships to say how they should run. \
  The order is decided by dependencies (tasks in the same level of depedency will run at the same time)

  ![img](img/basic-dag.png)

* `Task` \
  A Task is the basic unit of execution in Airflow. \
  Tasks are arranged into DAGs, and then have upstream and downstream dependencies set between them into order to express the order they should run in.
* `Operator` \
  An Operator is conceptually a template for a predefined Task \
  The idea behind an operator is to reuse code that can action by setting the parameters.
  * Ex. Bash operator will execute the command and add the parameters to that command

Other concepts:

* `Task Instance` \
  Much in the same way that a DAG is instantiated into a DAG Run each time it runs, the tasks under a DAG are instantiated into Task Instances.
* `Scheduler` \
  The Airflow scheduler monitors all tasks and DAGs, then triggers the task instances once their dependencies are complete.
* `Executor` \
  Executors are the mechanism by which task instances get run.
* `Metastore/Metadata Database` \
  Stores metadata about DAGs, tasks, task instances, and other Airflow components. \
  By default: SQLite, but it can be configured to use other databases such as MySQL, Postgres, or Oracle.
* `Web Server` \
  The Airflow Web Server is a component that provides a `web-based interface for interacting with Airflow`.
* `XCom` \
  Cross-communication is a feature that enables tasks to exchange messages, data, or metadata between them.

#### Airflow's Executor Modes

Determine how tasks are executed across a cluster of worker nodes.

* `Local Executor`
  * `Single-node` executor
  * Task are `sequentially` on the same machine as scheduler
  * `Limited` concurrency
  * `Simpler` to setup and maintain
  * Good for `smaller` deployments or testing environments

    ![img](documentation_images/local.png)

* `Celery Executor`
  * `Distributed` executor
  * Uses `Celery` for messaging and manage workers
  * Tasks are executed in `parallel` on worker nodes
  * `High` scalability and concurrency
  * Recommended for `large` deployments where high concurrency is needed

    ![img](documentation_images/celery.gif)

>These are not the only executor modes, however they are the most common.

### Airflow Docker Compose file

* `Postgres` \
  It's the Metastore Database
* `Redis` \
  Cache used for Apache Airflow's Celery Executor.
* `Airflow Web Server` \
  The web server for Apache Airflow's web interface.
  * It can be accessed at <http://localhost:8080>
* `Airflow Scheduler` \
  Runs DAGs and monitors task execution.
* `Airflow Worker` \
  Executes tasks assigned by the scheduler.
* `Airflow Triggerer` \
  Responsible for triggering the scheduling of DAG runs.
* `Airflow CLI` \
  Interface for interacting with the Airflow  via command-line
* `Airflow Flower UI` \
  Web-based monitoring tool for Celery workers.
  * It can be accessed at <http://localhost:5555>
* `Airflow Init` \
  Sets up initial configuration parameters when the containers are started.
  * It will go off when all other services are up

  ![img](documentation_images/celery-2.png)

## What You Will Learn

* ETL Concepts
* Airflow Components
* Airflow DAGs

## Practice

Suppose you are working on an Ad Company that process data from the users to then know what is the best suitable ad to give them when they are navigating on the internet.

The company is receiving JSON files from the user events, and they want you to transform them to CSV format because later they want to load it into a Database.

![img](documentation_images/ias.png)

### Requirements

Use the infrastructure created during the pre-setup to:

* Review the 2 airflow DAG's on `./dags/scripts` folder
  * Extract: `1_extract.py`
  * Transform: `2_transform.py`

* Based on these files
  * Create a new task `Load`
  * Read the output of `2_transform.py`
  * Write to console an insert query for each row
    * Asume table name is `event` and columname matches with dataframe column name
  * Save file as CSV in output folder `output.csv`
  * Remove intermediate files

### Step 1 - Extract (Parquet file)

>When you are building a big data environment sometimes you need to use other formats that may be more optimal than json or csv, the other 2 main types are `avro` and `parquet`
>
>*In another lesson we will go deep into these and other formats, for now, just have in mind that these are related to big data and datawarehouses*

The DAG on file `1_extract`, does the following

* Read the file `./input/sample.json`
* Convert to parquet format
* Save it to `./output/sample.parquet`

#### What is airflow doing behind the hood?

* Read the file (on `dags` folder) and check if there are no syntax errors to show the DAG in the list
  * If some error appear, the DAG will not be listed, instead you will get a banner with the error
* Check for configuration if DAG should be triggered
  * On the code:

  ```py
  default_args = {
    'owner': 'airflow',
    'depends_on_past': False, # It does not depends on any other actions/DAG
    'start_date': datetime(2022, 3, 1), # When should be triggered
    'retries': 0, # How many retries if fails
    'retry_delay': timedelta(minutes=5) # Wait before launch retry
  }
  ```

  >A DAG that was suppouse to run in the past will not be triggered, we can change to daily, every hour...

* Goes to idle state, waiting for a manual run
* After you execute a manual run
* The `WebUI` will queue an instruction to the `scheduler`
* The scheduler will send an instruction to the `executor` and remove from schedule
* The executor will create a `Task Instance`
* The task instance will run and will update the results to the `Metastore`

Since all the services: `WebUI`, `Scheduler`, `Executor`, `Task Instance` are polling the metastore and dags folders, all will be updated at the same time of the `Run Status`

![img](documentation_images/dag-3.png)

#### Manual run - Parquet DAG

* Go to Airflow Web UI
  * Login with `airflow`/`airflow`
* Search for the DAG and clic the `play` icon
* Select `Trigger DAG`

You should now see a file in `output` folder, when you open it you will see the contents of the file

>It may look the same as the input, but what are viewing is not the parquet file but the decoded parquet file. \
>You have this view because of the extension you installed during the pre-setup.
>
>The real parquet file is unreadable.

To view the real content:

* Right click on the parquet file
* Select `Open With...`
* Select `Text Editor` (Built in)
* You will get a warning `The file is not displayed in the text editor because it is either binary or uses an unsupported text encoding.`
* Click `Open Anyway`
* Select `Text Editor` (Built in)

### Step 2 - Transform (XComs)

>XComs (short for “cross-communications”) are a mechanism that let Tasks talk to each other, as by default Tasks are entirely isolated and may be running on entirely different machines.
>
>The contents on the XComs are serialized, you can pass anything as long as it's serialized.

The file `2_transform.py` is the same as `1_extract` with some modifications:

* `json2parquet` now returns `return file_output`
  * This allow XComs to pull this information
* You have now an additional task: `parquet_transform`
* Task transform depends on extract `extract > transform`
* Transform takes the `output` fo extract the nread it and add additional columns
* Transform have an additional parameter on definition
  `op_kwargs={'parquet_file': "{{ task_instance.xcom_pull(task_ids='Extract', key='return_value') }}"},`

  * op_kwargs \
    (Similar to kwargs) is a dictionary of keyword arguments that will get unpacked in your function
    * In this case we are mapping to the paremeter `parquet_file`
  * task_ids \
    Which task we are pulling the information
    * In this case we are pulling from the task `Extract`
  * key \
    Which field we are searching the data
    * In this case we are using the `return_value` (`return file_output`)

>Note we are defining the engine when reading since this is an encoded file

### Step 3 - Load

>In a real life scenario this step would include inserting into a datawarehouse or moving the files to another location for data mining or datalake, but to keep things simple in this lesson we will print and save as csv

The file `3_etl.py` contains a copy of `2_transform.py` that we will be adding to complete the requirements

1. Create a new task `Load`
    * Add dummy function

    ```py
    def parquet2csv(parquet_colums_file):
      pass
    ```

    * Declare the new task Operator

    ```py
      load = PythonOperator(
        task_id='Load',
        python_callable=parquet2csv,
        op_kwargs={'parquet_colums_file': "{{ task_instance.xcom_pull(task_ids='Transform', key='return_value') }}"},
        provide_context=True
      )
    ```

    * Add Task Dependency
      * Use the operator name declared above: `load`

    ```py
    extract >> transform >> load
    ```

2. Read the output of `Transform` task
      * Use Xcom for parameter of the function `parquet_colums_file`
      * Pull the value from `return` of `Transform` task

    ```py
    op_kwargs={'parquet_colums_file': "{{ task_instance.xcom_pull(task_ids='Transform', key='return_value') }}"}
    ```

3. Write to console an insert query for each row
    * Add code to the function to read the file

    ```py
    def parquet2csv(parquet_colums_file):
      file_input = parquet_colums_file
      df = pandas.read_parquet(file_input, engine='pyarrow')
    ```

    * Write to console an insert query for each row

    ```py
    for _, row in df.iterrows():
      print(f'''INSERT INTO event (year, month, day, user_id, x_coordinate, y_coordinate)
      VALUES ({row["year"]}, {row["month"]}, {row["day"]}, {row["user_id"]}, {row["x_coordinate"]}, {row["y_coordinate"]});''')
    ```

4. Save file as CSV in output folder `output.csv`

    ```py
    file_output = os.path.join(AIRFLOW_HOME, "dags", "output",  "output.csv")
    df.to_csv(file_output)
    ```

5. Remove intermediate files
    * We already have on XCom the file from step 2, add the file from step 1

    ```py
    op_kwargs={
      'parquet_colums_file': "{{ task_instance.xcom_pull(task_ids='Transform', key='return_value') }}",
      'parquet_file': "{{ task_instance.xcom_pull(task_ids='Extract', key='return_value') }}"
    }
    ```

    * Add the relevant code to the function to delete those 2 files

    ```py
    # Add the additional parameter
    def parquet2csv(parquet_file, parquet_colums_file):
      ...
      # Add the code to delete the files at the end of the function
      os.remove(parquet_file)
      os.remove(parquet_colums_file)
    ```

## Homework (Optional Investigation) - Explore the airflow Web UI

In Step 3 we `print some INSERT statements`

* Navigate airflow WebUI to get those logs
* Navigate the docker mounted folders to get those logs
* Navigate the project folders to get those logs

## Conclusion

In this practice, you learned how to configure Apache Airflow using Docker Compose and how to create DAGs and ETL workflows in Apache Airflow. By using Apache Airflow and Docker Compose, you can build robust and scalable ETL workflows that can be easily monitored and maintained.

## Still curious

* Airflow is the most common open source orchestrator for data pipelinesm, however it has more uses, some additional uses of airflow may include:
  * DevOps and Infrastructure Automation
  * ETL (Extract, Transform, Load)
  * Content Management
  * Finance and Billing
  * Healthcare and Medical Data
  * Manufacturing and Supply Chain
  * IoT (Internet of Things)
  * Compliance and Regulatory Reporting
  * Business Process Automation
  * Educational Institutions

>`Note:` As a general rule, if you can use a CRON like service, airflow can help you to do the same. But be careful, there are additional tools that may suite better your needs depending on what you are planning to use.

* What are airflow XComs?

  The idea behind XCom is that you can reuse some output as part of your next task in the thread.

  But you also need to be careful, this data is serialized and as you imagine, this also consumes memory.

  * How to use them efficiently?

    Imagine you need to process 10 files in a folder

    * For the first task you add the hash id
    * For the second task you calculate the sum between 2 columns
    * For the third task you save the file into a cloud

    The common sense is telling me to serialize the dataframe and pass it between tasks, but with this we are serializing data/deserializing using more memory than we need.

    The solution is to output the name of the file instead and save the file at the end of each step.

    This solution not only is more efficient, but also ensures if something goes wrong I can restart from the step that went wrong.

  Article: [Airflow XComs][xcoms]

## Links

### Used during this session

* [Pre Setup][pre-setup]
* [Install Docker][install_docker]

* [Airflow XComs][xcoms]

### Reinforce Lesson and homework help

* Documentation: [Core Concepts][airflow_core_concepts]
* Article: [Airflow Core Concepts][airflow_core_concepts_art]
* Article: [ETL Concepts][etl_concepts]
* Article: [AVRO VS Parquet][avro_vs_parquet]
* Article: [OPKwArgs and other Task parameters][op_kwargs]
* Article: [*args & **kwargs][args_kwargs]

[pre-setup]: ./pre-setup.md
[install_docker]: https://docs.docker.com/engine/install/

[xcoms]: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html

[airflow_core_concepts]: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/index.html
[airflow_core_concepts_art]: https://blog.knoldus.com/core-concepts-of-apache-airflow/
[etl_concepts]: https://learndatamodeling.com/blog/etl-concepts/
[avro_vs_parquet]: https://www.snowflake.com/trending/avro-vs-parquet/
[op_kwargs]: https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/python/index.html#airflow.operators.python.task
[args_kwargs]: https://realpython.com/python-kwargs-and-args/
