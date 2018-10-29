import pandas as pd
from ar4ds.core import *

raw_data = [{'title': 'Employee' , 'salary': 60.0}, 
         {'title': 'Employee' , 'salary': 60.0},
         {'title': 'Employee' , 'salary': 60.0},
         {'title': 'Manager' ,'salary': 100.0},
         {'title': 'Manager' ,'salary': 500.0},
         {'title': 'Manager' ,'salary': 90.0}]

data = pd.DataFrame(raw_data, columns=['title','salary'])

dc = compile(rule="implies(conj(eq(s.title, 'Manager'), eq(t.title, 'Employee')), gt(s.salary, t.salary))")

print(dc[data]["usually"])

#explain why


