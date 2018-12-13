import pandas as pd
from itertools import combinations
from ar4ds.core import *

def rolldown(prov, dc, modal):

    for k in range(1,len(prov['hidden'])+1):

        results = []
        for comb in combinations(prov['hidden'], k):
            
            comb = list(comb)

            test =   _eval(prov['data'], 
                     prov['aggcol'], 
                     prov['groupby']+comb, 
                     prov['agg'],
                     dc, modal)

            if not test[2]:
                results.append(test)

        if len(results) >= 1:
            return results

    return []

def _eval(data, col, perm, agg, dc, modal):
    output, _ = query(data, groupby=perm, col=col, withfn=agg)
    truth = dc[output]
    return (data, truth, truth[modal])





