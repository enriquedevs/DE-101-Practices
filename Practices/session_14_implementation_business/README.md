# Implementation for business

# Practice
Given the data in the class' S3 under "products", 
load it to your snowflake account and do the following queries

### Considerations

- you should create the given CDCs and their respective facts and dims
- this whole practice is performance oriented
- performance doesn't mean efficiency
- for you not reading all the files: products may have changes between years, 
your CDC must be able to capture the name of the products.
- Your client supplies the data for A-G companies, but you have one user
per company.
- create your facts and dims as you consider according to the next exercises.
- This is the year name configuration:
```
"Space Separated": [1980, 2000]
"PascalCase": [2001, 2015]
"Hyphen-Case": [2016, 2022]
```
- if something is not clear, you can ask your teacher or their assistants.

### Exercises

- users A, B and E want to get the utilities per every decade of
every product, keeping track of it even through the name changes.
- users F and G want to know the amount of sales that a product has every year,
but they don't want to keep track of the product name changes.
- users C and D want to know all the information for all the products.
- users A, D, F and E want to separate their data by state.
