# Pre-Setup

We will be using the Azure account created in the previous [lesson][prev_lesson]

## Requirements

### Azure database tables

>Create 4 tables in your azure database: AAPL_landing, AAPL, FRED_GDP_landing, FRED_GDP

* Go to SSMS or Azure Data Studio
* Select the database you created before ("data101-db")
* Open a new query and run:

  ```sql
  CREATE TABLE AAPL_landing (
      "Date" varchar(200),
      Low varchar(200),
      "Open" varchar(200),
      Volume varchar(200),
      High varchar(200),
      "Close" varchar(200),
      "Adjusted Close" varchar(200)
  );

  CREATE TABLE FRED_GDP_landing (
      "Date" varchar(200),
      "Value" varchar(200)
  );

  CREATE TABLE AAPL (
      "Date" date,
      Low float,
      "Open" float,
      Volume float,
      High float,
      "Close" float,
      "Adjusted Close" float
  );

  CREATE TABLE FRED_GDP (
      "Date" date,
      "Value" float
  );
  ```

### Azure Datawarehouse Table

>Create the "AAPL_landing" table also in your data warehouse ("AdventureWorksDW").

* Go to Data Studio
* Under your connection: drop down the database list
* Right click on your DW and select a new query

  ![img](documentation_images/data_studio_db_newquery.png)

* Run:

  ```sql
  CREATE TABLE AAPL_landing (
      "Date" varchar(200),
      Low varchar(200),
      "Open" varchar(200),
      Volume varchar(200),
      High varchar(200),
      "Close" varchar(200),
      "Adjusted Close" varchar(200)
  );
  ```

## Links

[Previous lesson][prev_lesson]

[prev_lesson]: ../session_16_ELT/README.md
