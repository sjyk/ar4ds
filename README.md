# ar4ds
Automated Reasoning For Data Science

## Contributors and Acknowledgements
This project is maintained by the University of Chicago Database Group under P.I Sanjay Krishnan. This work is in part supported by a generous equipment grant from NVIDIA. Student contributors include:
* Amy Zeng

## Motivation
Data analysis tools today give us quantitative query results. For example,
```
SELECT AVG(salary) as asal, position FROM employees GROUP BY position
```
might result in a table that looks like this:

| asal      | position        |
|-----------|-----------------|
| 44987.34  | Employee 1      |
| 88745.10  | Manager 1       |
| 24317.45  | Subcontractor 1 |
| 106672.98 | Manager 2       |


