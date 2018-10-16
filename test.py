import pandas as pd
from ar4ds.core import *

raw_data = [{'a': 'New York',     'b': 'NY'},
            {'a': 'New York',      'b': 'NY'},
            {'a': 'San Francisco', 'b': 'SF'},
            {'a': 'San Francisco', 'b': 'SF'},
            {'a': 'San Jose',      'b': 'SJ'},
            {'a': 'New York',      'b': 'NY'},
            {'a': 'San Francisco', 'b': 'SF0'},
            {'a': 'Berkeley City', 'b': 'Bk'},
            {'a': 'San Mateo',     'b': 'SM'},
            {'a': 'Albany',        'b': 'AB'},
            {'a': 'San Mateo',     'b': 'SM'}]

data = pd.DataFrame(raw_data, columns=['a','b'])

dc = compile(rule="implies( eq(s.b, t.b), eq(s.a, t.a))", 
             pre="eq(s.b, 'SFO')")

print(dc[data]["always"])




