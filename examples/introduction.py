from _examples import *
import pandas as pd

"""
Introduction to the rule engine
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

#3. Analysis question: why is new york's salary higher than sf?
from ar4ds.core import *

#Write an assertion in our language:
code = '''implies(conj(eq(s.branch,'NY'), eq(t.branch,'SF')), 
                  gt(s.salary, t.salary))'''
#Being in the NY branch implies that your salary is higher.
#Compile the code
dc = compile(code)

#4. Evaluate the expression
print("Does being in New York always imply higher salary?")
#Does being in New York always imply higher salary (no)
print(dc[data]["always"])
#record id of the exceptions
print(dc[data].exceptions)
exceptions = list(dc[data].exceptions)
#get exceptions
print(data.iloc[exceptions,:])
print()

#But that's not exactly what we want. Controlling for the position
#is it true that NY is higher than SF in salary?
print("Controlling for titles: ")
code = '''implies(conj(conj(eq(s.branch,'NY'), eq(t.branch,'SF')), eq(s.title, t.title)) , gt(s.salary, t.salary))'''
dc = compile(code)
print(dc[data]["always"])









