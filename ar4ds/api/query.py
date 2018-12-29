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

from .provenance import SchemaProvenance
from .lang import *

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

    output = data.groupby(groupby).agg({col: withfn}).reset_index()
    
    return output, SchemaProvenance(data, withfn, groupby, col)


def compile(rule="True", optimizer=QueryOptimizer):
    """Takes a String written in the ar4ds DSL and returns a DC object.

    DC objects are optimized executors for the ar4ds DSL. The compile function
    takes in a rule written in our syntax and creates a DC object. The DC object
    is provided query optimizer. The default optimizer executes it naively with 
    a nested loop join (not always the best for all expressions).

    Args:
        rule (String): A string ar4ds rule
        optimizer (ar4ds.opt.QueryOptimizer): A query optimizer

    Returns:
        output (ar4ds.dc.DC): A denial contstraint object

    """
    return DC(preprocess(rule), optimizer)


def validateDC(prov, dc, modal=1.0):
  """Given a query result validateDC returns any exceptional provanance.

  validateDC explores whether a DC not only holds on the query result but
  also any subaggregates (additional group by attributes). It has a modal 
  qualifier (modal) which thresholds the rule-to-exception ratio to detect
  such anomalies. When it does find such a refinement that violates the DC
  it returns. Right now this is implemented with a BFS, could probably be 
  smarter.

  Args:
        prov (ar4ds.api.provenance): A provenance object
        dc (ar4ds.dc.DC): A compiled DC expression
        modal (String/Float): A modal of how well the expression should hold

    Returns:
        None if valid, otherwise

        prov (ar4ds.api.provenance): Provenance of the failing subgroup query
        output (pd.DataFrame): Failed subgroup query
        truth (ar4ds.dc.ModalConstraint): Particular constraint that violated
  """

  #A helper method to evaluate a query for a certain validation
  def _eval(data, col, perm, agg, dc, modal):
    output, prov = query(data, groupby=perm, col=col, withfn=agg)
    truth = dc[output]
    return (prov, output, truth, truth[modal])


  #Executes the BFS
  for k in range(1,len(prov.hidden)+1):

      results = None
      for comb in combinations(prov.hidden, k):
          
          comb = list(comb)

          test =   _eval(prov.data, 
                         prov.col, 
                         prov.groupby+comb, 
                         prov.withfn,
                         dc, modal)

          if not test[3] and results == None:
              results = test
          elif not test[3] and \
                  len(results.exceptions) < len(test[1].exceptions):
              results = test

      if results != None:
          return results[0], results[1], results[2]

  return None


def assertDC(prov, dc, modal=1.0):
  """Tests to see if validateDC is None (i.e., invalid)
  """
  return (validateDC(prov, dc, modal) == None)






