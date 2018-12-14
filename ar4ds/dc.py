# -*- coding: utf-8 -*-
"""Represents the optimized Denial Constraint objects and their evaluation.

This module does most of the work in this package right now. It creates and 
optimizes the DC expressions. That part is a little clunky really only supports
pushdown and hash join optimizations but we can do more complex re-writes at a 
higher level.

DCs are also lazy--hence the two classes in the module.
"""

from .core import *


#There are some human readable modal logic constants
#SK wants to have an undergrad build and NLP interface
NEVER = 'never'
OCCASIONALLY = 'occasionally'
USUALLY = 'usually'
ALWAYS = 'always'
NECESSARY = 'necessary'
POSSIBLE = 'possible'


class DC(object):
    """
    """


    def __init__(self, rexp, optimizer):
        self.rule = eval('lambda s,t: ' + rexp)
        self.rexp = rexp
        self.optimizer = optimizer


    def getRange(self, dataset, conds, left):
        ranges = set()

        if len(conds) == 0:
            return set(range(len(dataset)))

        for i in range(len(dataset)):

            for c in conds:

                if left:
                    exp = eval('lambda s: ' + c)
                else:
                    exp = eval('lambda t: ' + c)

                if exp(dataset.iloc[i]):
                    ranges.add(i)

        return ranges


    def explainPlan(self, dataset):
        opt = self.optimizer(dataset)
        plan = opt.plan(self.rexp)
        precond = eval('lambda s,t: ' + plan['pre'])
        
        rules = set(range(len(dataset)))
        exceptions = set()

        if len(plan['s']) > 0:
            print("Pushing down:\n\t",plan['s'])

        if len(plan['t']) > 0:
            print("Pushing down:\n\t", plan['t'])

        if len(plan['pre']) > 0:
            print("Implication Left Prune:\n\t", plan['pre'])

        if len(plan['st']) > 0:
            print("Hash Join on:\n\t", plan['st'])
        else:
            print("Nested Loop Join:\n\t", "S x T\n\t\t")

    def __getitem__(self, dataset):

        opt = self.optimizer(dataset)
        plan = opt.plan(self.rexp)
        precond = eval('lambda s,t: ' + plan['pre'])
        
        rules = set(range(len(dataset)))
        exceptions = set()

        lrange = self.getRange(dataset, plan['s'], True)
        rrange = self.getRange(dataset, plan['t'], False)

        for i in lrange:
            s = dataset.iloc[i]
            
            for j in rrange:
                t = dataset.iloc[j]

                if not precond(s,t) or i == j:
                    
                    if (i in rules):
                        rules.remove(i)
                    
                    if (j in rules):
                        rules.remove(j)

                    continue

                if self.rule(s,t):
                    pass
                else:
                    exceptions.add(i)
                    exceptions.add(j)

        return ModalConstraint(rules.difference(exceptions), exceptions)



    def __str__(self):
        return self.rexp







class ModalConstraint(object):

    def __init__(self, rules, exceptions):
        self.rules = rules
        self.exceptions = exceptions

    def __getitem_frac__(self, t):
        if len(self.rules) == 0 and len(self.exceptions) == 0:
            return False

        else:
            frac = (len(self.rules) + 0.0) /(len(self.rules) + len(self.exceptions))
            return (frac >= t)

    def __getitem__(self, modal):

        try:
            f = float(modal)
            return self.__getitem_frac__(f)
        except:
            pass

        if len(self.rules) == 0 and len(self.exceptions) == 0:
            return (modal == ALWAYS)

        if len(self.rules) == 0:
            return (modal == NEVER)
        
        if len(self.rules) > 0:
            if len(self.exceptions) == 0:
                return (modal == NECESSARY) or \
                       (modal == ALWAYS) or    \
                       (modal == POSSIBLE) or \
                       (modal == USUALLY)

            if len(self.rules) > len(self.exceptions):
                return (modal == USUALLY) or \
                       (modal == POSSIBLE)
            else:
                return (modal == OCCASIONALLY) or \
                        (modal == POSSIBLE)

