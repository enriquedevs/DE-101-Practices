# Reporting Bases

>Reporting Bases: Base (Usually raw) data or datasources used for generating reports in BI and Data Analytics.

In this lesson we will explore a BI or visualization tool (such as Tableau or the one of your preference)

## Exercises

Using the already created views from the last session:

* Connect your database with your BI tool
* Create as many reports as you consider

## BI Tools

**Business Intelligence (BI) tools** are software applications that help organizations analyze, visualize, and gain insights from their data. These tools enable businesses to make informed decisions by transforming raw data into meaningful and actionable information. BI tools often provide features such as data integration, querying, reporting, dashboarding, and analytics.

Some popular BI tools include:

* **Tableau**: A powerful and user-friendly tool for data visualization and analysis, Tableau allows users to create interactive and shareable dashboards that provide insights into various aspects of the business.
* **Microsoft Power BI**: A suite of business analytics tools that helps users create interactive visualizations, reports, and dashboards. Power BI offers seamless integration with other Microsoft products, making it a popular choice for organizations using Microsoft solutions.
* **QlikView/Qlik Sense**: Qlik offers two BI products, QlikView and Qlik Sense. Both provide a platform for data discovery, visualization, and analysis, with Qlik Sense focusing on self-service analytics and a modern, responsive interface.
* **Looker**: A cloud-based BI platform that provides data exploration, visualization, and reporting capabilities. Looker is known for its ability to integrate with a wide range of data sources and its scalable architecture.
* **SAP BusinessObjects**: A comprehensive BI suite that offers tools for reporting, analysis, and data visualization. SAP BusinessObjects caters to a wide range of users, from business analysts to IT professionals, and integrates well with SAP's other enterprise software solutions.

![image](resources%2Fbi-tools-2.png)

![image](resources%2Fbi-tools-3.png)

## Data Engineering VS Data Science

Data Engineering and Data Science are two related, yet distinct fields within the broader data domain. They both deal with data but focus on different aspects of the data lifecycle and require different skill sets.

### Data Engineering

Data Engineering primarily focuses on the design, development, and management of data infrastructure, pipelines, and systems. The main objective of data engineering is to ensure that data is collected, stored, processed, and made available to other teams or applications efficiently and reliably. Data engineers are responsible for:

1. **Building and maintaining data pipelines**: Data engineers create processes that collect, transform, and load (ETL) data from various sources into data storage systems, such as data warehouses or data lakes.
2. **Data storage and management**: They design and optimize database systems, data warehouses, and data lakes to store and manage data efficiently.
3. **Data quality and consistency**: Data engineers ensure data quality by implementing processes to clean, validate, and standardize data. They also handle data governance and ensure that data complies with organizational policies and regulations.
4. **Data integration**: They facilitate the integration of data from different sources and make it accessible to other teams or applications.
5. **Performance optimization**: Data engineers work to optimize data processing and query performance to ensure data can be analyzed effectively and in a timely manner.

### Data Science

Data Science focuses on extracting insights, knowledge, and patterns from data using various analytical, statistical, and machine learning techniques. Data scientists are responsible for:

1. **Data exploration and analysis**: Data scientists explore and analyze data to identify trends, patterns, and relationships that can provide valuable insights for decision-making.
2. **Statistical modeling and machine learning**: They develop and apply statistical models and machine learning algorithms to make predictions, classify data, or discover hidden patterns in the data.
3. **Data visualization**: Data scientists create visual representations of data to help stakeholders understand the insights and patterns identified in the analysis.
4. **Experimentation and hypothesis testing**: They design experiments and tests to validate hypotheses and evaluate the effectiveness of different strategies or solutions.
5. **Decision support**: Data scientists communicate their findings to stakeholders and help them make data-driven decisions.

## Conclusion

*Data engineering* cares about data transformation and quality (ETL, ELT...) and *Data science* uses that processed information to get value out of that information (Reports, BI, Querys...)

Reporting bases are created by Data Engineers, then are used by data scientists

## Still curious

We mention some BI tools today, however the most popular BI are Tableau and Power BI.

*What are the main differences?
*When will you choose one or the other?
*Which one is cheaper?
*Could you give a "no-brain" of a situation where you will pick:
  *Power BI
  *Tableu

You can use the following articles to try answer these questions:

*[Tableau vs. Power BI: The Better Choice in 2023?][tableau_vs_powerbi]
*[Power BI vs Tableau: Which Should You Choose in 2023?][which]
*[Power BI vs. Tableau: Top 10 Major Differences][differences]

[tableau_vs_powerbi]: https://geekflare.com/tableau-vs-power-bi/
[which]: https://www.datacamp.com/blog/power-bi-vs-tableau-which-one-should-you-choose
[differences]: https://intellipaat.com/blog/power-bi-vs-tableau-difference/
