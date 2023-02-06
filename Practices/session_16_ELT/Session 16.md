# ELT Environments and Database Integration Tools

In this practice we will setup the environment, tools and resources necesary for the following sessions.


### Prerequisites
* Azure Free Account ([Instructions]())
* Azure Data Studio or SQL Server Management Studio ([Data Studio](), [SSMS]())
* SQL Server for macos with Docker ([docker-compose.yml]())
* Nasdaq Free Account (API)
* Nasdaq api key file


### What you will learn
* How to create resources on Azure Portal
* How to connect to a Database in Azure
* How to connect to an HTTP source
* How to connect to a Datalake in Azure
* How to get data with a python script in Synapse
* ADF linked services
* How to create a Data Warehouse in Azure Synapse (runs sql dw (olap) and spark with "massively parallel programming" under the hood)



# Practice

You are a data engineer working for a credit rating agency. You need to get Stock Market Data every day, store it in a Data Warehouse for financial research and analysis for further publication. You work in the team responsible of getting data from the Nasdaq Index from different resources/formats


STEP 1

- Resource group
- Blob storage
- Data lake storage
- SQL Database server
- SQL Database
- Dedicated SQL Pool
- Azure Data Factory Workspace
- Synapse Workspace
- 