from ar4ds.core.rulesClasses import *
from ar4ds.core.processors import *
from ar4ds.core.ops import *

import pandas as pd

data = pd.DataFrame([{'id':0, 'a': 1, 'b': 2}, {'id':1, 'a': 2, 'b': 4}], columns=['id','a','b'])
data.set_index(['id'], inplace=True)

e = Expression(HasProperty('a',1), HasProperty('a',2), BooleanExpression('b', GT))
r = Rule(e, data, Naive())

#print(filter(data, data.a == 1))
out = agg(data, 'a', 'b', ['mean'])
print(r.supports(out.iloc[0], out.loc[1], 'mean(b)'))
