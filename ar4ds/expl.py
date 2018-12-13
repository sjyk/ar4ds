import pandas as pd
from itertools import combinations
from ar4ds.core import *

def assertDC(prov, dc, modal=1.0):
    return (validateDC(prov, dc, modal) == None)

def validateDC(prov, dc, modal=1.0):

    for k in range(1,len(prov['hidden'])+1):

        results = None
        for comb in combinations(prov['hidden'], k):
            
            comb = list(comb)

            test =   _eval(prov['data'], 
                     prov['aggcol'], 
                     prov['groupby']+comb, 
                     prov['agg'],
                     dc, modal)

            if not test[2] and results == None:
                results = test
            elif not test[2] and \
                    len(results.exceptions) < len(test[1].exceptions):
                results = test

        if results != None:
            return results

    return None

def _eval(data, col, perm, agg, dc, modal):
    output, prov = query(data, groupby=perm, col=col, withfn=agg)
    truth = dc[output]
    return (prov, truth, truth[modal])





