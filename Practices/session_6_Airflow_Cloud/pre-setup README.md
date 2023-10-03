# Pre-setup

## Cloud Computing

![img](documentation_images/cloud-2.png)

Cloud computing is the delivery of on-demand computing resources, such as servers, storage, databases, software, and analytics, over the internet.

>Rather than owning and maintaining physical servers and infrastructure, users can access these resources from cloud service providers.

In this course we will be using some cloud providers, but for this specific lesson we will be using Amazon Web Services (AWS)

### Amazon Web Services (AWS)

AWS is a the cloud provided by Amazon.com, the services it offers can help you build, deploy and manage your infrastructure and their applications.

***AWS Regions**: Whenever you are making usage of AWS you will be using some specific Region resources, which means you decide where your application will be hosted.
  Each Region is identified by a code name, such as us-east-1 (North Virginia), eu-west-1 (Ireland), and ap-southeast-2 (Sydney).
***AWS Availability Zones**: Inside these regions the load is distributed, the idea is to have an architecture when if one goes down the other availability zones are still up.

![img](documentation_images/cloud-5.png)

As you may imagine being AWS has equivalent of some services you may already know and some custom services available

Here are some most important services on AWS:

***IAM (Identity and Access Management)**: This will allow you to manage security; Permission, policies, roles, users...
***RDS (Relational Database Service)**: Cloud relational data, some flavors you can pick are: MySQL, PostgreSQL, and Oracle.
***CloudWatch**: Log collection, monitoring and audit service.
***DynamoDB**: Non-relational database, you can still use mongo or similar if you do the wiring as a custom service, but out of the box this is the one.
***EC2 (Elastic Compute Cloud)**: Virtual machine service, if you have something dockerized just upload the image and select the output ports.
***S3 (Simple Storage Service)**: This will be your File system for almost everything, even if you upload an image to the container registry for EC2 it will still use S3 in the backend.
***VPC (Virtual Private Cloud)**: This will create a connection between your services, so you don't need to worry for interconecction security such as firewalls in your app components. You can customize this as much as you want with routing tables...

![img](documentation_images/cloud-7.png)

Other AWS important concepts are:

***IAM User**: Represents a person or an application that needs to access AWS resources
***AWS Roles**: AWS roles are entities that you can create in IAM to define a set of permissions for a specific task or job function.
***IAM Policies**: They specify which AWS resources can be accessed and what actions can be taken on those resources.
***AWS CLI**: AWS CLI is a command-line tool that enables you to interact with AWS services using commands in your terminal or shell.
***AWS Console**: The AWS console is a web-based user interface that allows users to interact with AWS services and manage their AWS resources.

![img](documentation_images/cloud-8.png)

## Composer

Run the docker-compose yml that start docker containers for Airflow:

```sh
docker-compose up -d
```

The provided Docker Compose file is a YAML file that describes the services required for Apache Airflow to run. The file
consists of several services, each of which is defined as a container:

***Postgres**: A relational database that stores metadata for Apache Airflow (It's the Metastore Database).
***Redis**: An in-memory data structure store used for Apache Airflow's Celery Executor.
***Airflow Web Server**: The web server for Apache Airflow's web interface. It can be accessed at **<http://localhost:8080>**
***Airflow Scheduler**: The scheduler for Apache Airflow that runs DAGs and monitors task execution.
***Airflow Worker**: The worker that executes tasks assigned by the scheduler.
***Airflow Triggerer**: Component that is responsible for triggering the scheduling of DAG runs.
***Airflow CLI**: Component that provides an interface for interacting with the Airflow command-line interface (CLI).
***Airflow Flower UI**: Component that provides a web-based monitoring tool for Celery workers. It can be accessed at **<http://localhost:5555>**
***Airflow Init**: This Service sets up initial configuration parameters when the containers are started. It also runs database migrations and creates the administrator account.
