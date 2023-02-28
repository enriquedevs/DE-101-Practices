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

### Amazon Web Services (AWS)

AWS is a cloud computing platform that offers a wide range of services to help businesses and individuals build, deploy, and manage their applications and infrastructure in the cloud.

Here are some most important concepts about AWS:

+ **AWS Regions**: An AWS Region is a physical location where AWS has multiple data centers. AWS currently has over 25 Regions around the world. Each Region is identified by a code name, such as us-east-1 (North Virginia), eu-west-1 (Ireland), and ap-southeast-2 (Sydney).
+ **AWS Availability Zones**: Within each Region, AWS has multiple Availability Zones (AZs). An AZ is a distinct data center with its own power, networking, and connectivity.

![img](documentation_images/cloud-5.png)


Here are some most important services on AWS:

+ **IAM (Identity and Access Management)**: IAM is a service that enables you to manage access to AWS resources securely. You can create and manage users, groups, and roles and assign permissions to them using IAM policies.
+ **RDS (Relational Database Service)**: RDS is a managed database service that makes it easy to set up, operate, and scale a relational database in the cloud. With RDS, you can choose from several popular database engines, such as MySQL, PostgreSQL, and Oracle, and run them on scalable and highly available infrastructure.
+ **CloudWatch**: CloudWatch is a monitoring service that provides real-time metrics and logs for AWS resources and applications.
+ **DynamoDB**: DynamoDB is a fully managed NoSQL database service that provides low-latency, high-throughput access to structured and unstructured data.
+ **EC2 (Elastic Compute Cloud)**: EC2 is a scalable virtual machine service that enables you to launch and manage virtual servers in the cloud.
+ **S3 (Simple Storage Service)**: S3 is an object storage service that provides durable, scalable, and secure storage for any type of data. It's like a Filesystem Cloud Service.
+ **VPC (Virtual Private Cloud)**: VPC is a networking service that enables you to create a virtual private network in the cloud. With VPC, you can control your network environment, including IP addresses, subnets, and routing tables, and securely connect to other AWS resources or on-premises infrastructure.

![img](documentation_images/cloud-7.png)

Other AWS important concepts are:

+ **IAM User**: IAM user is an entity within AWS that represents a person or an application that needs to access AWS resources
+ **AWS Roles**: AWS roles are entities that you can create in IAM to define a set of permissions for a specific task or job function. Roles can be assigned to AWS services or AWS users to grant permissions to access AWS resources.
+ **IAM Policies**: IAM policies are documents that define permissions for a specific user, group, or role. They specify which AWS resources can be accessed and what actions can be taken on those resources.
+ **AWS CLI**: AWS CLI is a command-line tool that enables you to interact with AWS services using commands in your terminal or shell.
+ **AWS Console**: The AWS console is a web-based user interface that allows users to interact with AWS services and manage their AWS resources.

![img](documentation_images/cloud-8.png)

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