# -*- coding: utf-8 -*-
"""This module describes the internal api for "set" explanations.

A set explanation is a predicate derived from a set of row ids.
"""
import pandas as pd

def _is_number(dt):
    return (dt == 'int64' or dt == 'float64')

def _min_max(df):
    return (df.min(), df.max(), df.max()-df.min())

def _num_hist(df, stats , bins=10):
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
            histograms.append(_num_hist(subset[c], _min_max(df[c]) ))
        else:
            histograms.append(subset[c].value_counts(normalize=True))

    return histograms

def _diff(h1, h2):

    out = []

    for v in h1.index.values:
        h1[v] = h1.get(v, 0) - h2.get(v, 0)

    return h1


def histdiff(df, rows):
    hist1 = hist(df)
    hist2 = hist(df, rows)

    output = []

    for h1,h2 in zip(hist1, hist2):
        output.append(_diff(h1,h2))

    return output