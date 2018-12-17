# -*- coding: utf-8 -*-
"""
Our default query optimizer is based on the Cascades
optimizer. 

Graefe, Goetz. "The cascades framework for query optimization." 
IEEE Data Eng. Bull. 18.3 (1995): 19-29.

The cascades query optimizer is a top-down query optimizer that 
is based on transformations. We adopt the same architecture for 
ar4ds.
"""

from .opt import *


class CascadesParseOptState(object):
    """Defines a helper object that holds the optimization state

    Attributes:
        expr (String): The function call
        arity (Set[String]): {}, {s}, {t}, {s,t}
        n_arity (int): len(arity)
        s (List[String]): list of s push downs
        t (List[String]): list of t push downs
        st (List[String]): list join conditions
    """

    def __init__(self, code, s,t, st):
        self.expr = getExpression(code)
        self.arity = getArity(code)
        self.n_arity = len(self.arity)
        self.s = s
        self.t = t
        self.st = st
        self.code = code



class CascadesQueryOptimizer(QueryOptimizer):
    """Defines the Cascades query optimizer for DC evaluation

    Basic structure:
    * The framework executes a list of rules that transform the query
    by s,t,st pushdowns

    * Rules are allowed to be recursive (all pushdowns on subqery a or b)
    """

    def __init__(self, data):

        """List of rules. 

        Each rule is a tuple (a,b), where a is a boolean function
        of CascadesParseOptState, and b appends a transformation
        to s,t,st lists.
        """
        self.rules = [ (self._indivisible_expr, self.break_pth),\
                       (self._unitary_expr, self.base_pth),\
                       (self._divisible_expr, self.recurse_pth)]

        super().__init__(data)

    def _unitary_expr(self, state):
        return (state.n_arity == 1)

    def _indivisible_expr(self, state):
        return (state.expr != 'conj' and state.n_arity == 2)

    def _divisible_expr(self, state):
        return (state.expr == 'conj' and state.n_arity == 2)

    def break_pth(self,state):
        state.s.append(None)
        state.t.append(None)
        state.st.append(None)

    def base_pth(self,state):
        if 's' in state.arity:
            state.s.append(state.code)
        else:
            state.t.append(state.code)

    def recurse_pth(self, state):
        b1, b2 = splitBinary(state.code) 
        s1,t1,st1 = self.getPushDownRules(b1)
        s2,t2,st2 = self.getPushDownRules(b2)

        state.s.extend(s1 + s2)
        state.t.extend(t1 + t2)
        state.st.extend(st1 + st2)

    def getPushDownRules(self, code):
        s = []
        t = []
        st = []

        state = CascadesParseOptState(code, s, t, st)

        #rolling out the rules
        for rule, opt in self.rules:
            if rule(state):
                opt(state)

        return s,t,st


    def plan(self, code):
        pre = self.getPrecondition(code)
        s,t,st =  [], [], []

        if pre != "True":
            s,t,st = self.getPushDownRules(pre)

        if None in s or None in t or None in st:
            return {'s':[], 't':[], 'st':[], 'pre': pre}
        else:
            return {'s':s, 't':t, 'st':st, 'pre': pre}