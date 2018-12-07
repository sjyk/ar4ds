import pandas as pd
from ar4ds.core import *

def rolldown(prov, dc, modal):
    return _rolldown(prov['data'], 
                     prov['aggcol'], 
                     prov['groupby']+prov['hidden'], 
                     prov['agg'],
                     dc, modal)

def _rolldown(data, col, perm, agg, dc, modal):
    results = []

    for i,j in enumerate(perm):
        print(col)
        output, _ = query(data, groupby=perm[0:i+1], col=col, withfn=agg)
        
        try:
            truth = dc[output]
        except:
            truth = None

        results.append((output, truth))

        if truth != None or not truth[modal]:
            return results, True

    return results, False



