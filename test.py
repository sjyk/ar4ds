import pandas as pd
from ar4ds.core import *
from ar4ds.expl import *

raw_data = [{'title': 'Employee', 'branch':'SF' , 'salary': 60.0}, 
         {'title': 'Employee' , 'branch': 'SF', 'salary': 60.0},
         {'title': 'Employee', 'branch': 'NY' , 'salary': 50.0},
         {'title': 'Manager' , 'branch': 'SF','salary': 300.0},
         {'title': 'Manager', 'branch':'NY' ,'salary': 290.0},
         {'title': 'Manager', 'branch':'NY' ,'salary': 90.0},
         {'title': 'Sub' , 'branch': 'SF','salary': 10.0},
         {'title': 'Temp', 'branch': 'SF' ,'salary': 20.0},
         {'title': 'Manager', 'branch': 'NY' ,'salary': 40.0}]

data = pd.DataFrame(raw_data, columns=['title','branch', 'salary'])
df, prov = query(data, groupby=["branch"], col="salary", withfn="mean")
#print(df)
dc = compile("implies(conj( eq(s.branch,'NY'), eq(t.branch,'SF')), gt(s.salary, t.salary))", pre="conj( eq(s.branch,'NY'), eq(t.branch,'SF'))")
print(rolldown(prov, dc, "0.0"))

#dc = compile("implies(conj( eq(s.title,'Employee'), eq(t.title,'Manager')), gt(t.salary, s.salary))")
#print(dc[data]["usually"], dc[df]["usually"])




