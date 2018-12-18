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
    """The definition of a Denial Constraint (DC) object.

    A DC expresses that a set of predicates cannot be true together
    for any combination of tuples in a relation. It can be thought of
    as a generalization of functional dependencies. 

    Here is a formal definition. Let R be a set of tuples, and let C = R X R
    be a set of *pairs* of tuples. A DC is a constraint on the cross product
    C. All DCs can be trivially evaluated by expanding the cartesian product.
    The query optimizer's job is to avoid doing this.

    In general, DCs can be any boolean function over the pairs. In practice
    our application only considers boolean functiosn that start with implies or iff
    (convince yourself deduction is pointless if it wasn't this).

    DC's are lazy in the sense that the are not realized until you apply them
    to a dataset. We allow for both static and dynamic optimizations.

    Example usage
    >>> code='''implies(conj( eq(s.branch,'NY'), eq(t.branch,'SF')), 
                        gt(s.salary, t.salary))
             '''
    >>> dc = compile(code, CascadesQueryOptimizer)
    >>> data[data]
    """

    def __init__(self, rexp, optimizer):
        """Constructor for a DC object.

        In our DSL, rules are lambda expressions over pairs of tuples s,t.
        By convention s denotes the left tuple and t denotes the right tuple.

        Args:

            rexp (String): A DC rule in our DSL.
            optimizer (QueryOptimizer): A query optimizer object
        """
        self.rule = eval('lambda s,t: ' + rexp)
        self.rexp = rexp
        self.optimizer = optimizer


    def __getitem__(self, dataset):
        """This method defines the evaluation interface for a DC

        Args:
            dataset (pd.DataFrame): Dataset is a pandas DataFrame.

        Returns:
            output (ModalConstraint): The dc grounded on particular data
        """

        opt = self.optimizer(dataset)
        plan = opt.plan(self.rexp)
        precond = eval('lambda s,t: ' + plan['pre'])
        
        rules = set(range(len(dataset)))
        exceptions = set()

        lrange = self._getRange(dataset, plan['s'], True)
        rrange = self._getRange(dataset, plan['t'], False)

        for i in lrange:
            s = dataset.iloc[i]

            precond_fail = True
            
            for j in rrange:
                t = dataset.iloc[j]

                if not precond(s,t) or i == j:
                    continue
                elif precond(s,t):
                    precond_fail = False

                if self.rule(s,t):
                    pass
                else:
                    exceptions.add(i)
                    exceptions.add(j)

            if precond_fail and (i in rules):
                rules.remove(i)

        return ModalConstraint(rules.difference(exceptions), exceptions)

    def _getRange(self, dataset, conds, left):
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
        """This is a hacky explain plan system for debugging to
        describe what the optimizer is actually doing.
        """

        opt = self.optimizer(dataset)
        plan = opt.plan(self.rexp)
        precond = eval('lambda s,t: ' + plan['pre'])
        
        rules = set(range(len(dataset)))
        exceptions = set()

        if len(plan['s']) > 0:
            print("->Pushing down:\t",plan['s'])

        if len(plan['t']) > 0:
            print("->Pushing down:\t", plan['t'])

        if len(plan['st']) > 0:
            print("\t->Hash Join on:\t", plan['st'])
            print("\t\t->Filter:\t", self.rexp)
        else:
            print("\t->Nested Loop Join:\t", self.rexp)

    def __str__(self):
        return self.rexp


class ModalConstraint(object):
    """A ModalConstraint describes a DC that has been applied to data

     Modal logic is a type of formal logic from the 1960s that extends 
     classical logic to include operators expressing modality. A modal is 
     a word that qualifies a statement (such as "usually")--more 
     specifically, quantifies the fraction of possible worlds a 
     statement is true.

     Our ModalConstraint objects index records that support and violate a 
     specific dc in two attributes (rules and exceptions).

     Example usage:

     >>out = data[data]
     >>out[0.5] #are at least half of the tuples in satisfaction
     >>out["usually"] #^ same as above
     >>out[1.0] #are all the tuples in satisfaction
     >>out["always"] #^ same as above
    """

    def __init__(self, rules, exceptions):
        """Constructor

        Args:
            rules (Set[Int]): A set of row index that satisfy the dc
            exceptions (Set[Int]): A set of indexes that violate the dc
        """
        self.rules = rules
        self.exceptions = exceptions


    def __getitem_frac__(self, t):
        if len(self.rules) == 0 and len(self.exceptions) == 0:
            return False

        else:
            frac = (len(self.rules) + 0.0) /(len(self.rules) + len(self.exceptions))
            return (frac >= t)


    def __getitem__(self, modal):
        """
        Syntactic sugar to make usage easy.
        """

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

