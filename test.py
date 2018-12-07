import pandas as pd
from ar4ds.core import *
from ar4ds.expl import *

raw_data = [{'title': 'Employee', 'id':1 , 'salary': 60.0}, 
         {'title': 'Employee' , 'id':1, 'salary': 60.0},
         {'title': 'Employee', 'id':1 , 'salary': 60.0},
         {'title': 'Manager' , 'id':4,'salary': 100.0},
         {'title': 'Manager', 'id':4 ,'salary': 500.0},
         {'title': 'Manager', 'id':4 ,'salary': 90.0},
         {'title': 'Sub' , 'id':3,'salary': 10.0},
         {'title': 'Temp', 'id':3 ,'salary': 20.0},
         {'title': 'Manager', 'id':4 ,'salary': 40.0}]

data = pd.DataFrame(raw_data, columns=['title','id', 'salary'])
df, prov = query(data, groupby=["id"], col="salary", withfn="mean")
print(prov)
dc = compile("implies(conj( eq(s.id,'Employee'), eq(t.id,'Manager')), gt(t.salary, s.salary))")
print(rolldown(prov, dc, "usually"))

#dc = compile("implies(conj( eq(s.title,'Employee'), eq(t.title,'Manager')), gt(t.salary, s.salary))")
#print(dc[data]["usually"], dc[df]["usually"])

"""
#whyeq(data,'title',3,4)

for rule, pre in whyie(data,'salary',0,1):
    print(rule)
    dc = compile(rule=rule, pre=pre)
    print(dc[data]["usually"])
    #print(len(dc[data].rules) + len(dc[data].exceptions))

#explain why
"""


