# -*- coding: utf-8 -*-
"""This module describes the internal api for "set" explanations.

A set explanation is a predicate derived from a set of row ids. We
implement a histogram-based approach that builds histograms on each 
attribute and finds predicates that best explain differences between
the histograms.
"""
import pandas as pd

from ar4ds.opt import splitBinary, getExpression
from ar4ds.dc import DC

##Helper Methods

def _is_number(dt):
    '''
    Helper function to determine if a column is a number
    '''
    return (dt == 'int64' or dt == 'float64')

def _min_max(df):
    '''
    Calculate the range of a numeric column
    '''
    return (df.min(), df.max(), df.max()-df.min())

def _num_hist(df, stats, bins):
    '''
    Calculate a histogram with the specified number of bins
    '''

    hist = [0]*bins

    mn, mx, rng = stats
    step = rng/(bins-1)
    N = len(df)

    for i in range(N):
        v = int((df.iloc[i] - mn)/step)
        hist[v] += 1.0/N

    df = pd.DataFrame([((mn+step*i, mn+step*(i+1)) ,v) \
                        for i, v in enumerate(hist)], 
                        columns=['bucket','value'])

    return df.set_index('bucket', drop=True)['value']

def _diff(h1, h2):

    out = []

    for v in h1[1].index.values:
        h1[1][v] = h1[1].get(v, 0) - h2[1].get(v, 0)

    return (h1[0],h1[1])



def _histdiff(df, rows, bins, numerical):
    hist1 = hist(df, None, bins, numerical)
    hist2 = hist(df, rows, bins, numerical)

    output = []

    for h1,h2 in zip(hist1, hist2):
        output.append(_diff(h1,h2))

    return output



def _significant_positive_difference(h, thresh):
    
    N = len(h)
    factor = thresh/N
    name, hist = h

    exp = "False"
    score = 0.0

    for ind in hist.index.values:
        if -hist[ind] > factor:
            exp = "disj({},{})".format(exp,_index_to_pred(name, ind))
            score += -hist[ind]
        elif hist[ind] > factor:
            exp = "disj({},neg({}))".format(exp,_index_to_pred(name, ind))
            score += hist[ind]

    return (score, exp)

def _index_to_pred(name, ind):
    if isinstance(ind, str):
        s = "eq(s.{}, {})".format(name, ind)
        t = "eq(t.{}, {})".format(name, ind)

        return "conj({},{})".format(s,t)

    elif isinstance(ind, tuple):
        s = "inr(s.{}, {},{})".format(name, ind[0], ind[1])
        t = "inr(t.{}, {},{})".format(name, ind[0], ind[1])

        return "conj({},{})".format(s,t)




## Public methods


def hist(df, rows, bins, numerical):

    histograms = []

    subset = df

    if rows != None:
        subset = df.iloc[rows,:]

    for c,d in zip(df.columns.values,df.dtypes):
        if _is_number(d) and numerical:
            histograms.append((c,_num_hist(subset[c], _min_max(df[c]), bins)))
        else:
            histograms.append((c,subset[c].value_counts(normalize=True)))

    return histograms



def predicate(df,rows, thresh=2.0, bins=10, numerical= True):
    histograms = _histdiff(df, rows, bins, numerical)

    pfilter = None

    for h in histograms:
        pred = _significant_positive_difference(h,thresh)
        if pred[1] != 'False':
            if pfilter == None or pred[0] > pfilter[0]:
                pfilter = pred

    return pfilter


def restrict(df, rows, dc, thresh=2.0, bins=10, numerical=True):

    exp = getExpression(dc.rexp)

    if exp == None or exp != 'implies':
        raise ValueError("Cannot run deduction engine over " + dc.rexp)

    a, b = splitBinary(dc.rexp)
    rfilter = predicate(df,rows, thresh, bins, numerical)

    if rfilter == None:
        return None

    a = "conj({},{})".format(rfilter[1],a)

    return DC("implies({},{})".format(a,b), dc.optimizer)





    
