# Interview Readiness

As a recruiter, the following common areas are evaluated while hiring new Data Engineers:

1. **Focus on problem-solving skills**: Senior data engineers must be able to identify problems and come up with solutions. Ask candidates about their approach to solving complex data engineering problems, and ask them to walk you through their thought process.
2. **Ask about their experience with data storage and processing technologies**: Candidates should have hands-on experience with technologies like Hadoop, Spark, Kafka, and NoSQL databases. Ask them about specific projects they have worked on using these technologies.
3. **Assess their knowledge of data modeling and database design**: Candidates should have a good understanding of database design principles and be able to create efficient data models. Ask them to describe the process they follow when designing a database schema.
4. **Check their familiarity with data security and compliance**: Candidates should have experience with data security and compliance regulations. Ask them about the measures they take to ensure data security and privacy.
5. **Assess their ability to communicate technical concepts**: Senior data engineers should be able to communicate technical concepts to non-technical stakeholders. Ask candidates to explain a complex data engineering concept to you as if you were a non-technical stakeholder.
6. **Look for candidates with experience in data pipeline development and deployment**: Candidates should have experience with designing, building, and deploying data pipelines. Ask them about their experience with ETL tools and techniques.
7. **Assess their familiarity with cloud platforms**: Senior data engineers should be familiar with cloud platforms like AWS, Azure, or GCP. Ask them about their experience with deploying and managing data engineering workflows on these platforms.
8. **Look for candidates with a passion for learning**: Technology is constantly evolving, and data engineering is no exception. Look for candidates who are passionate about learning and staying up-to-date with the latest trends in data engineering.

## Commonly Asked Questions

* Batch VS Streaming
* OLTP VS OLAP
* Designing an OLTP Database
* Designing an OLAP or Datawarehouse Database
* ETL VS ELT
* DDL VS DML
* Transaction Concept
* Commit and Rollback
* Lambda Architecture and ETLs Architectures
* View VS Materialize View
* Datawarehouse, Datamart and Datalake concepts
* Datalake partitions
* Star and Snoflake schemas
* Types of data load: Truncate and reload, Incremental/Delta/Upsert, Append
* Designing end to end ETL
* Designing end to end ELT
* Algorithm problem solving, common used algorithms are: 
1. Binary Search
2. Bubble Sort
3. Merge Sort
4. Quick Sort
5. Selection Sort
6. Insertion Sort
7. Depth-First Search (DFS)
8. Breadth-First Search (BFS)
9. Dijkstra's Algorithm
10. Dynamic Programming (DP)
11. Recursion
12. Binary Tree Traversal (Pre-order, In-order, Post-order)
13. Hash Tables and Hashing Algorithms

Here is a resource to know the implementation of the algorithms: https://www.youtube.com/watch?v=shs0KM3wKv8&list=PLOuZYwbmgZWXvkghUyMLdI90IwxbNCiWK

* SQL Queries:
1. Joins (LEFT, RIGHT, INNER, OUTER)
2. Distinct
3. Group By
4. Having
5. CTE (Common Table Expressions)
6. Window Functions
7. Subqueries

## Big O notation

Big O notation is a mathematical notation used to describe the time and space complexity of algorithms. Time complexity describes how the running time of an algorithm grows with respect to the input size, while space complexity describes how much memory an algorithm uses with respect to the input size.

Time complexity is denoted by the letter "O" followed by a function that represents the upper bound of the running time of the algorithm. For example, if an algorithm takes a constant time to run, we write O(1); if it takes time proportional to the size of the input, we write O(n); and so on. The "O" in Big O notation stands for "order of magnitude."

Space complexity is also denoted by the letter "O" followed by a function that represents the upper bound of the memory used by the algorithm. For example, if an algorithm uses a constant amount of memory, we write O(1); if it uses memory proportional to the size of the input, we write O(n); and so on.

Here are some common time and space complexities and their descriptions:

Time complexity:

* **O(1)**: Constant time. The algorithm takes a constant amount of time to run regardless of the input size.
* **O(log n)**: Logarithmic time. The algorithm's running time increases logarithmically as the input size grows larger.
* **O(n)**: Linear time. The algorithm's running time increases linearly as the input size grows larger.
* **O(n log n)**: Quasilinear time. The algorithm's running time increases almost linearly as the input size grows larger.
* **O(n^2)**: Quadratic time. The algorithm's running time increases quadratically as the input size grows larger.

Space complexity:

* **O(1)**: Constant space. The algorithm uses a constant amount of memory regardless of the input size.
* **O(log n)**: Logarithmic space. The amount of memory used by the algorithm increases logarithmically as the input size grows larger.
* **O(n)**: Linear space. The amount of memory used by the algorithm increases linearly as the input size grows larger.
* **O(n^2)**: Quadratic space. The amount of memory used by the algorithm increases quadratically as the input size grows larger.

When analyzing the time and space complexity of an algorithm, we typically focus on the worst-case scenario, as this gives us the upper bound of the algorithm's performance. By understanding the time and space complexity of an algorithm, we can choose the most appropriate algorithm for a given problem and optimize algorithms for better performance.

## Common Interview formats

The format very commonly it is asked to do a design from an scenario of a OLTP or OLAP database and then do queries about the design. Here are resources to practice those:

- https://leetcode.com
- https://www.hackerrank.com


Also it is asked sometimes a coding challenge on the strongest language to solve a problem, here are resources to practice those

- https://www.hackerrank.com/domains/sql