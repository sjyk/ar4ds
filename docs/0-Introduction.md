# Introduction
Consider the folowing database query:
```
SELECT AVG(salary) as asal, position FROM employees GROUP BY position
```
This query result in an output that looks like this:

| asal      | position        |
|-----------|-----------------|
| 44987.34  | Associate 1      |
| 88745.10  | Manager 1       |
| 24317.45  | Subcontractor 1 |
| 106672.98 | Manager 2       |

This result implicitly defines a set of logical assertions--manager 1 employees on average make more than associate 1 employees, or manager 2 employees have an average salary of 106672.98. For the most part, in today's data analysis tools these assertions are always quantitatively *correct*; assuming that the data itself is correct. 

To a human, quantitative results are not sufficient to justify conclusions. The statement, manager 1 employees on average make more than associate 1 employees, can be true for many different qualitative reasons. For example, the statement could mean that either "it is usually true that a manager 1 employee makes more than an associate 1 employee" or "due to a small number of very high earners, the average manager 1 employee salary is higher than that of associate 1 employees." The challenge is that systems today cannot reason about soft rules and their exceptions. On one extreme we have constructs based in pure prepositional or predicate logic (yes/no questions) and on the other extreme we have systems based in pure probabilistic logic (requires a complete model of the world).

## Loading Data


