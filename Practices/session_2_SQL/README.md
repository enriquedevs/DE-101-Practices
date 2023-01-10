# SQL Overview and Relational DBs on Containers Practice

In this practice we will manipulate data on a Relational Database within a Docker container

![Docker-Mysql](documentation_images/docker-mysql.png)

### Prerequisites
* [Install docker](https://docs.docker.com/engine/install/) 
* Install a db client (i.e. [DBeaver](https://dbeaver.io/download/)) 

### What You Will Learn
- How to use a docker container of a relational database
- Docker commands
- Operative System commands and Overview
- How to connect to a Docker Container
- How to connect to a Database by using a DB client
- SQL Overview
- Transactions Overview

# Practice

You're working on a clinic, and the clinic needs a database to have records of the appointments that were made between the patient and the doctor.

The clinic only provides you an excel file with the historical data of the appointments and they ask you to create the database from it.

![clinic](documentation_images/clinic.jpeg)


### Requirements
- Develop and setup a docker container of a Relational Database by using the provided [excel](https://dbeaver.io/download/) file's data
- Normalize on Third Normal Form (3NF) the Database
- Execute requested queries from the database

# Let's do it!

## Step 1

Check the Excel file and create an initial definition of the database on a SQL file

## Step 2

Create within this folder a Dockerfile with the following content:

```
FROM mysql
ENV MYSQL_ROOT_PASSWORD mypassword
ADD clinic_db.sql /docker-entrypoint-initdb.d
EXPOSE 3306
```
