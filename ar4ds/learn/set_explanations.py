# -*- coding: utf-8 -*-
"""This module describes the internal api for "set" explanations.

A set explanation is a predicate derived from a set of row ids.
"""
import pandas as pd


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

def _num_hist(df, stats , bins=10):
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


def hist(df, rows=None):

    histograms = []

    subset = df

    if rows != None:
        subset = df.iloc[rows,:]

    for c,d in zip(df.columns.values,df.dtypes):
        if _is_number(d):
            histograms.append((c,_num_hist(subset[c], _min_max(df[c]) )))
        else:
            histograms.append((c,subset[c].value_counts(normalize=True)))

    return histograms

def _diff(h1, h2):

    out = []

    for v in h1[1].index.values:
        h1[1][v] = h1[1].get(v, 0) - h2[1].get(v, 0)

    return (h1[0],h1[1])


def histdiff(df, rows):
    hist1 = hist(df)
    hist2 = hist(df, rows)

    output = []

    for h1,h2 in zip(hist1, hist2):
        output.append(_diff(h1,h2))

    return output


def _significant_positive_difference(h, thresh=1.5):
    
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


def predicates(df,rows):
    histograms = histdiff(df, rows)

    filters = []

    for h in histograms:
        pred = _significant_positive_difference(h)
        if pred[1] != 'False':
            filters.append(pred)

    filters.sort()

    return filters


    
