# Implementation for Business

## Practice

Given the data in the class S3 under "products":

* Load it to your snowflake account and do the following queries:
  * Users A, B and E want to get the utilities per every decade of every product, keeping track of it even through the name changes.
  * Users F and G want to know the amount of sales that a product has every year, but they don't want to keep track of the product name changes.
  * Users C and D want to know all the information for all the products.
  * Users A, D, F and E want to separate their data by state.

### Considerations

* Create the given CDCs and their respective facts and dims
* This whole practice is performance oriented
  >Performance doesn't mean fast, instead getting the best possible results
* For you not reading all the files:
  * Products may have changes between years
  * CDC must be able to capture the name of the products.
* Your client supplies the data for A-G companies, but you have one user per company.
* Create your facts and dims as you consider according to the next exercises.
* This is the year name configuration:

  ```txt
  "Space Separated": [1980, 2000]
  "PascalCase": [2001, 2015]
  "Hyphen-Case": [2016, 2022]
  ```

>If something is not clear, you can ask your teacher or their assistants.
