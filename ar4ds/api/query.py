# -*- coding: utf-8 -*-
"""This module contains the user-facing query and explanation API.

Attributes:
    query(...): runs a group by aggregate query on a data frame

    compile(...): interprets and optimizes an expression written in our dsl

    validateDC(...): given a query result validates a compiled expression

    assertDC(...): calls validateDC but has as interface similar to assert()
"""
from ar4ds.opt import *
from ar4ds.dc import *

import pandas as pd
from itertools import combinations


def query(data, groupby, col, withfn):
    """The query function runs a group by aggregate on a PD DataFrame

    query() takes a data frame, a grouping, a desired aggregate, and 
    an aggregation function and calls pandas to perform the query. The
    key reason that it is separate right now is to track provenance. It
    returns a separate provenance object with information about the query
    derivation.

    Args:
        data (pd.DataFrame): A Pandas DataFrame
        groupby (List[String]): A list of strings of columns to group with
        col (String): A single column to aggregate
        withfn (String): A string pandas aggregate function

    Returns:
        output: A DataFrame representing the output of the group by aggregate
        provenance: A dictionary describing the logical provenance
    """

    def _removeall(l1, l2):
        return [l for l in l1 if not l in l2]

    all_cols = list(data.columns.values)
    all_cols = _removeall(all_cols, groupby)
    all_cols = _removeall(all_cols, [col])

    output = data.groupby(groupby).agg({col: withfn}).reset_index()
    
    provenance = {'data': data,
                  'agg': withfn,
                  'groupby': groupby,
                  'aggcol': col,
                  'hidden': all_cols}

    return output, provenance


def compile(rule="True", optimizer=QueryOptimizer):
    return DC(rule, optimizer)


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





