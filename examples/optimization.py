from _examples import *
import pandas as pd

from ar4ds.api import *
from ar4ds.core import *

"""
Introduction to the query optimizer
"""

data = pd.DataFrame(raw_data, columns=['title','branch', 'salary'])
code = '''implies(conj(eq(s.branch,'NY'), eq(t.branch,'SF')), gt(s.salary, t.salary))'''

#1. ar4ds uses a query optimizer to optimize the evaluation of the rules
#you can see how a rule is being evaluated with
dc = compile(code)
print("Rule evaluated with a nested loop join: \n")
dc.explainPlan(data)
#executes the evaluation with a nested loop join

print("\n\n")

from ar4ds.opt.cascades import CascadesQueryOptimizer
#2. you can add more sophisticated optimizers:
dc = compile(code, CascadesQueryOptimizer)
print("Cascades finds push down optimizations: \n")
dc.explainPlan(data)







