from ar4ds.core.rulesClasses import *
from ar4ds.core.processors import *
import pandas as pd

data = pd.DataFrame([{'id':0, 'a': 1, 'b': 2}, {'id':1, 'a': 1, 'b': 4}], columns=['id','a','b'])
data.set_index(['id'], inplace=True)

e = Expression(HasProperty('a',1), HasProperty('a',1), BooleanExpression('b', EQ))
r = Rule(e, data, Naive(), kModalSystem)

print(r)
