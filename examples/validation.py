from _examples import *
import pandas as pd

from ar4ds.api import *
from ar4ds.core import *

"""
Introduction to the validation system
"""

data = pd.DataFrame(raw_data, columns=['title','branch', 'salary'])

#1. Print the raw data
print("The loaded data is: ")
print(data)
print()

#2. Run a group by aggregate query (group mean salary by branch)
from ar4ds.api import *
output, prov = query(data, groupby=["branch"], col="salary", withfn="mean")
print("The query result is: ")
print(output)
print()

#3. Why is the average higher? handles uncertainty
code = '''implies(conj(eq(s.branch,'NY'), eq(t.branch,'SF')), gt(s.salary, t.salary))'''
dc = compile(code)
print("Does being in New York usually imply higher salary?")
print(dc[data]["usually"])
print()

#4. Does this trend validate?
print("Is this trend sound?")
print(assertDC(prov, dc, "usually"))


print()

data = pd.DataFrame(raw_data_hidden, columns=['title','branch', 'salary'])

#5. Print the raw data where correlations are changed
print("The loaded data is: ")
print(data)
print()

#6. Run a group by aggregate query (group mean salary by branch)
from ar4ds.api import *
output, prov = query(data, groupby=["branch"], col="salary", withfn="mean")
print("The query result is: ")
print(output)
print()

#7. Does the previous trend validate?
print("Is this trend sound?")
print(assertDC(prov, dc, "usually"))
print()

#8. Why not? SK: API should be cleaned up here
print("What is the issue?")
_, output, eval_dc = validateDC(prov, dc, "usually")
exceptions = list(eval_dc.exceptions)
print(output.iloc[exceptions, :])


