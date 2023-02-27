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

### Cloud Computing
Cloud computing is the delivery of on-demand computing resources, such as servers, storage, databases, software, and analytics, over the internet. Rather than owning and maintaining physical servers and infrastructure, users can access these resources from cloud service providers like Amazon Web Services (AWS), Microsoft Azure, or Google Cloud Platform.

Cloud service providers offer several benefits, including **scalability, flexibility, cost-effectiveness, and enhanced security**, making cloud computing an attractive option for businesses of all sizes.

![img](documentation_images/cloud-2.png)

### Software as a Service (SaaS)

SaaS is a software delivery model where the software application is hosted by the service provider and made available to the users over the internet. Users can access the software through a web browser or app, and the provider handles all the maintenance and updates.

AWS offers several SaaS solutions, including Amazon Chime, a communication and collaboration service, and Amazon WorkDocs, a secure content creation, storage, and collaboration service.

![img](documentation_images/cloud-3.jpeg)

### Platform as a Service (PaaS)

PaaS is a cloud computing model that provides developers with a platform to build, deploy, and manage applications without having to worry about infrastructure. The provider handles the underlying infrastructure, including servers, storage, and network, while the developer can focus on building and deploying their application.

AWS offers several PaaS solutions, including AWS Elastic Beanstalk, a service that makes it easy to deploy and run applications, and AWS Lambda, a serverless computing service.

![img](documentation_images/cloud-4.png)

### Infrastructure as a Service (IaaS)

IaaS is a cloud computing model that provides users with access to virtualized computing resources over the internet. The provider offers virtualized servers, storage, and network infrastructure that users can provision and manage.

AWS offers several IaaS solutions, including Amazon Elastic Compute Cloud (EC2), a service that provides resizable compute capacity in the cloud, and Amazon Simple Storage Service (S3), a scalable object storage service.

![img](documentation_images/cloud-3.png)

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