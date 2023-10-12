# SQL Reporting

You will learn about sql querying for data reporting.

## Practice

Use the generator script to produce the data for your practice.

In this practice we will focus on producing queries and storing them into views.

### Considerations

* Create the needed fact and dimensions tables as you consider.
* Every query should be stored in a view.
* Don't mix Companies in your results.
* Every query should be stored in a `create_views.sql` in your own branch.

### Exercises

1. Select the price and product for every state and month.
2. Select the amount of sales by product-year for every state.
3. Select the month with the highest sales for every product.
4. Select the month with the lowest sales for every product.
5. Get the most sold category for every company.
6. Get the total sales (in money) for a company in every state.

## Still curious

You want more SQL exercises?

* [Exercism PL/SQL][exercism]
* [HackerRank SQL][hackerrank]
* [Letetcode Database][leetcode]

Improve your SQL readability:

* [10 Best Practices to Write Readable and Maintainable SQL Code][sql_good_practices]
* [Best practices for writing SQL queries][sql_best_practices]

[exercism]: https://exercism.org/tracks/plsql/exercises
[hackerrank]: https://www.hackerrank.com/domains/sql
[leetcode]: https://leetcode.com/problemset/database/

[sql_good_practices]: https://towardsdatascience.com/10-best-practices-to-write-readable-and-maintainable-sql-code-427f6bb98208
[sql_best_practices]: https://www.metabase.com/learn/sql-questions/sql-best-practices
