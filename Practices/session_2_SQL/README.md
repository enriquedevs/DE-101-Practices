# SQL Overview and Relational DBs on Containers Practice

In this practice we will manipulate data on a Relational Database within a Docker container

![img](documentation_images/docker-mysql.png)

### Prerequisites

* [Install docker](https://docs.docker.com/engine/install/)
* Install a db client (i.e. [DBeaver](https://dbeaver.io/download/))
* Follow the [pre-setup guideline](pre-setup%20README.md)

### What You Will Learn

- How to use a docker container of a relational database
- Docker commands
- Operative System commands and Overview
- How to connect to a Docker Container
- How to connect to a Database by using a DB client
- SQL Overview
- Transactions Overview

# Practice

You're working on a clinic, and the clinic needs a database to have records of the appointments that were made between
the patient and the doctor.

The clinic only provides you a CSV file with the historical data of the appointments and they ask you to create the
database from it.

![img](documentation_images/clinic.jpeg)

### Requirements

- Develop and setup a docker container of a Relational Database by using the provided [CSV](clinic.csv) file's data

# Let's do it!

## Step 1

Now let's create a sample **´clinic_db´** within the mysql database.

First, let's connect to the docker container with the following command:

```shell
docker exec -it clinic-container bash
```

This command will connect to **´clinic_container´** on a bash console.

Now within docker container, with following command will connect to mysql instance:

```shell
mysql -u root -p
```

This command will ask you for a password and type: **mypassword**

Now let's create **´clinic_db´** on mysql with the following command:

```sql
create database clinic_db;
```

This command will create the database **´clinic_db´**

## Step 2

Following up, let's connect to the database by using a Database client, on this case with DBeaver.

First let's open [DBeaver](https://dbeaver.io/download/) IDE and click on the New Database Connection Icon that is on
the upper left of the IDE:

![img](documentation_images/dbeaver-1.png)

Then a pop up window will open and here selects **´MySQL´** option and click on **Next**

![img](documentation_images/dbeaver-2.png)

Then on connection parameters use the following:

+ Server Host: **localhost**
+ Port: **6603**
+ Database: **clinic_db**
+ Username: **root**
+ Password: **mypassword**

![img](documentation_images/dbeaver-3.png)

Then on Driver Properties tab on **´allowPublicKeyRetrieval´** set is as **´true´**

![img](documentation_images/dbeaver-4.png)

Now click on Test connection and should appear as **´Connected´**

![img](documentation_images/dbeaver-5.png)

## Step 3

Now let's check the CSV file data and create an initial definition of the database

In this case the provided [CSV](clinic.csv) file contains the following data:

```
patient_name,patient_last_name,patient_address,appointment_date,appointment_time,doctor_name,doctor_last_name,doctor_clinical_specialization
John,Doe,123 Main St,2022-01-01,10:00 AM,Jane,Smith,Pediatrics
Jane,Smith,456 Park Ave,2022-01-02,11:00 AM,Michael,Johnson,Family Medicine
Michael,Johnson,789 Elm St,2022-01-03,12:00 PM,Emily,Williams,Cardiology
Emily,Williams,321 Oak St,2022-01-04,1:00 PM,Matthew,Brown,Cardiology
Matthew,Brown,654 Pine St,2022-01-05,2:00 PM,Abigail,Jones,Dermatology
Abigail,Jones,987 Cedar St,2022-01-06,3:00 PM,Daniel,Miller,Orthopedics
```

On this case there are the following columns:

| Column Name                    | Data Type |
|--------------------------------|-----------|
| patient_name                   | String    |
| patient_last_name              | String    |  
| patient_address                | String    |
| appointment_date               | Date      | 
| appointment_time               | Time      | 
| doctor_name                    | String    | 
| doctor_last_name               | String    | 
| doctor_clinical_specialization | String    |

Now let's create a database table definition for this data:

```sql
create table clinic_raw (
    patient_name varchar(100),
    patient_last_name varchar(100),
    patient_address varchar(200),
    appointment_date varchar(50),
    appointment_time varchar(50),
    doctor_name varchar(100),
    doctor_last_name varchar(100), 
    doctor_clinical_specialization varchar(100)
);
```

To execute it on database, you can open dbeaver and execute it on a SQL Script tab:

![img](documentation_images/dbeaver-6.png)

## Step 4

Now let's load CSV data into the raw table.

First copy csv file from local to the container with the following command:

```shell
docker cp clinic.csv clinic-container:/tmp/clinic.csv
```

This command will copy local host **´clinic.csv´** file to clinic-container's **´/tmp/clinic.csv´**

Now let's connect to clinic_db with the command:

```shell
docker exec -it clinic-container mysql --local-infile=1 -u root -p
```

This command will connect to mysql db from the docker's **´clinic-container´** that we ran before.

* The mysql command option **´--local-infile=1´** will allow to import local files while executing SQL statements

Once on mysql prompt, let's set a global variable that will allow us to use local files from SQL statements by using the
following command:

```sql
SET GLOBAL local_infile=1;
```

Then switch to **´clinic_db´** with the following command:

```sql
USE clinic_db;
```

Once there, we can import CSV data to **´clinic_raw´** table with the following command:

```sql
LOAD DATA LOCAL INFILE "/tmp/clinic.csv"
INTO TABLE clinic_raw
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
```

This command did the following:

* **LOAD DATA LOCAL INFILE**: This specifies that the data to be loaded is in a file, and it should be loaded locally
  from the client machine, rather than from the server.
* **"/tmp/clinic.csv"**: This specifies the path to the CSV file that contains the data to be loaded.
* **INTO TABLE clinic_raw**: This specifies the name of the table in the database where the data should be loaded.
* **COLUMNS TERMINATED BY ','**: This specifies that the fields in the CSV file are separated by commas.
* **OPTIONALLY ENCLOSED BY '"'**: This specifies that each field in the CSV file may be enclosed in double quotes.
* **ESCAPED BY '"'**: This specifies that a double quote character within a field can be escaped by a double quote
  character.
* **LINES TERMINATED BY '\n'**: This specifies that each line in the CSV file is terminated by a newline character.
* **IGNORE 1 LINES**: This specifies that the first line of the CSV file should be ignored, as it typically contains
  headers or column names and is not part of the actual data to be loaded.

Now let's verify all csv data is present by using the following SQL statements:

```
select * from clinic_raw;
```

And following data will show:

![img](documentation_images/clinic-raw-table.png)

## Step 5
Normalization is a process of organizing data in a database to minimize redundancy and eliminate data anomalies. The process involves applying a set of rules called normal forms. The higher the normal form, the less redundancy and fewer anomalies the database has.

Here are the steps to normalize the clinic_raw table from the first normal form (1NF) to the third normal form (3NF):

### 1NF (Unnormalized Form)
- The clinic_raw table is in the unnormalized form (UNF) or 1NF because it contains repeating groups and multiple values in some of its columns.

### 2NF (First Normal Form)
- To convert the clinic_raw table to 2NF, we need to identify the functional dependencies between the columns.

- The patient name, last name, and address together uniquely identify a patient, so we can extract them into a separate table.

- The doctor name, last name, and clinical specialization together uniquely identify a doctor, so we can extract them into a separate table.

- The appointment date, time, patient name, last name, address, doctor name, last name, and clinical specialization together uniquely identify an appointment, so we can extract them into a separate table.

- After applying these steps, we will have three tables: Patient, Doctor, and Appointment.

### 3NF (Second Normal Form)
- To convert the clinic_raw table to 3NF, we need to identify and remove transitive dependencies between the columns.

- In the Appointment table, doctor_name, doctor_last_name, and doctor_clinical_specialization are all dependent on the doctor_id column. We can create a new Doctor table to remove this transitive dependency.

- Similarly, in the Appointment table, patient_name, patient_last_name, and patient_address are all dependent on the patient_id column. We can create a new Patient table to remove this transitive dependency.

### Let's write 

We need to create the data DDLs for our tables now that we know which are the problems with the clinic_raw.

So let's create the query for the Patient table. 

```sql
CREATE TABLE Patient
(
    patient_id        INT PRIMARY KEY,
    patient_name      VARCHAR(100),
    patient_last_name VARCHAR(100),
    patient_address   VARCHAR(200)
);

```

Now the Doctor table.

```sql
CREATE TABLE Doctor
(
    doctor_id                      INT PRIMARY KEY,
    doctor_name                    VARCHAR(100),
    doctor_last_name               VARCHAR(100),
    doctor_clinical_specialization VARCHAR(100)
);

```

And finally our main table "Appointment".

```sql
CREATE TABLE Appointment
(
    appointment_id   INT PRIMARY KEY,
    appointment_date DATE,
    appointment_time TIME,
    patient_id       INT,
    doctor_id        INT,
    FOREIGN KEY (patient_id) REFERENCES Patient (patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctor (doctor_id)
);
```

## HOMEWORK TIME !!!

Now that we have all of our new tables, we need to fill them. 
Make a script using sql to load your data from clinic_raw to the new tables.

Submit your SQL script on Canvas' Session 2 - Homework

# Conclusion

Docker is a powerful tool that makes it easy to run and manage databases like MySQL. By following this practice, you
should now have a solid understanding of how to use Docker to run and manage a MySQL container. Remember that Docker is
just one of many tools you can use to manage your databases, and that you should always choose the right tool for the
job.

I hope this guide was helpful in your understanding of using Docker with MySQL. You are now equipped with the knowledge
to deploy and manage your MySQL databases using Docker. Happy coding!