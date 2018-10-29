import pandas as pd
from ar4ds.core import *

raw_data = [{'title': 'Employee', 'id':4 , 'salary': 60.0}, 
         {'title': 'Employee' , 'id':4, 'salary': 60.0},
         {'title': 'Employee', 'id':4 , 'salary': 60.0},
         {'title': 'Manager' , 'id':4,'salary': 100.0},
         {'title': 'Manager', 'id':4 ,'salary': 500.0},
         {'title': 'Manager', 'id':4 ,'salary': 90.0}]

data = pd.DataFrame(raw_data, columns=['title','id', 'salary'])

print(query(data, groupby=["title"], col="salary", withfn="mean"))

dc = compile(rule="implies(conj(eq(s.title, 'Manager'), eq(t.title, 'Employee')), gt(s.salary, t.salary))")

print(dc[data]["usually"])

#explain why


