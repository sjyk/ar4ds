from _examples import *
import pandas as pd

from ar4ds.api import *
from ar4ds.core import *

"""
Introduction to the validation system
"""

#1. Load the data run a query
data = pd.read_csv('berkeley.csv')
output, prov = query(data, groupby=["Gender"], col="Admit", withfn="mean")
print("The query result is: ")
print(output)

#2. Write a rule to check
code = '''implies(conj(eq(s.Gender,'Male'), eq(t.Gender,'Female')), gt(s.Admit, t.Admit))'''
#Being in the Male implies a higher admittance rate.
#Compile the code
dc = compile(code)
print("Asserting trend", code)
print()

print("Is this trend sound?")
print(assertDC(prov, dc, "usually"))
print()

print("What is the issue?")
_, output, eval_dc = validateDC(prov, dc, "usually")
exceptions = list(eval_dc.exceptions)
print(output.iloc[exceptions, :])





