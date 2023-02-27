# Airflow and Cloud Introduction

In this practice we will develop a simple ETL pipeline on Airflow and start using cloud services on them.

![Docker-Python](documentation_images/cloud.png)

### Prerequisites
* [Install docker](https://docs.docker.com/engine/install/)

### What You Will Learn
- Airflow Components
- Airflow DAGs
- Cloud Concepts
- AWS Introduction

# Practice

Suppose you are working on an Ad Company that process data from the users to then know what is the best suitable ad to give them when they are navigating on the internet.

The company is receiving JSON files from the user events and those are stored on S3, and they want you to transform them to CSV format at S3 because later they want to load it into a Database.

![img](documentation_images/ias.png)


### Requirements
* Use Airflow to create an ETL pipeline to process JSON file into a CSV file at S3

# Let's do it!


## Step 1

Run the docker-compose yml that start docker containers for Airflow:
```
docker-compose up -d
```

### Understanding the Docker Compose file
The provided Docker Compose file is a YAML file that describes the services required for Apache Airflow to run. The file consists of several services, each of which is defined as a container:

* Postgres: A relational database that stores metadata for Apache Airflow.
* Redis: An in-memory data structure store used for Apache Airflow's Celery Executor.
* Airflow Web Server: The web server for Apache Airflow's web interface.
* Airflow Scheduler: The scheduler for Apache Airflow that runs DAGs and monitors task execution.
* Airflow Worker: The worker that executes tasks assigned by the scheduler.

The version field defines the version of Docker Compose that this file uses. The x-airflow-common section is an anchor that is reused by other services to specify common configurations. The environment section defines the environment variables used by Apache Airflow, such as the database connection string and Celery configurations. The volumes section maps the local directories to directories within the containers, and the user field specifies the user and group that run the container.

### Creating DAGs
DAGs (Directed Acyclic Graphs) are a collection of tasks that define a workflow in Apache Airflow. Each DAG defines a series of tasks and their dependencies, which the scheduler uses to determine the order of execution. The DAGs for Apache Airflow are stored in the ./dags directory, which is mapped to the /opt/airflow/dags directory in the Airflow Web Server and Airflow Scheduler containers.

To create a new DAG, create a new Python script in the ./dags directory. In the script, you can use the Python API provided by Apache Airflow to define your workflow.

### ETL in Apache Airflow
ETL (Extract, Transform, Load) is a process that involves extracting data from various sources, transforming the data into a desired format, and loading the transformed data into a destination database. Apache Airflow provides a flexible platform to build ETL workflows by allowing you to define tasks, dependencies, and execution order.

For example, to create an ETL workflow to extract data from a source database, transform the data, and load it into a destination database, you can define tasks for each of these steps using the Apache Airflow API and then specify the dependencies between the tasks.

# Conclusion

In this practice, you learned how to configure Apache Airflow using Docker Compose and how to create DAGs and ETL workflows in Apache Airflow. By using Apache Airflow and Docker Compose, you can build robust and scalable ETL workflows that can be easily monitored and maintained.urse has covered the basics of Numpy and Pandas, including setting up a virtual environment, reading in data, and performing transformations on that data. With these tools and techniques, you can begin working with large datasets and performing data analysis in Python.