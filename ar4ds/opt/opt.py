"""This module defines the basic primitives for a query optimizer.

Right now we use ast, astor, and asttokens. Astor is probably a waste
not that useful.
"""

import ast
import astor
import asttokens

def toAST(code):
    """Takes a string in the ar4ds dsl and returns an AST

    Args:
        code (String): A ar4ds code snippet

    Returns:
        output (ast.Tree): An abstract syntax tree representing the code
    """
    return ast.parse(code)

def toSource(ast):
    """Takes an AST and synthesizes the corresponding source

    Args:
        code (ast.Tree)

    Returns:
        output (code): A source code string
    """
    return astor.to_source(ast)


def getExpression(code):
    """Determines if the code consistutes a function call returns the fn

    Args:
        code (String): An ar4ds code snippet

    Returns:
        output (String): The ar4ds function call identifier, or None if invalid
    """
    tree = toAST(code)
    try:
        return tree.body[0].value.func.id
    except:
        return None


def getArity(code):
    """Determines if s or t show up in one or more of the subexpressions

    Args:
        code (String): An ar4ds code snippet

    Returns:
        output (set{s,t}): A subset of {s,t}, of which of the relations show up
    """

    tree = toAST(code)
    ids = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if node.id in ('s', 't'): 
                ids.add(node.id)

    return ids

def splitBinary(code):
    """Splits a binary expression into its constituent subexpressions

    Args:
        code (String): An ar4ds code snippet

    Returns:
        output1 (String): Subexpression 1
        output2 (String): Subexpression 2
    """
    atok = asttokens.ASTTokens(code, parse=True)
    calls = []

    for node in ast.walk(atok.tree):
        if isinstance(node, ast.Call):
            calls.append(atok.get_text(node))

    return calls[1], calls[2]




class QueryOptimizer(object):
    """Defines the basic structure of the query optimizer

    All query optimizers extend the QueryOptimizer object. At
    some level all DCs have the same logical query plan:
    filter(S x T)

    There are three basic types of optimizations:
    * Left pushdown:
    (f_s(S) x T) 

    * Right pushdown:
    (S x f_t(T))

    * Hash join:
    (S inner-join T)

    These optimizations are not mutually exclusive, and 
    it is the optimizer's job to find those optimizations
    that are most beneficial.
    """

    def __init__(self, data):
        self.data = data


    def getPrecondition(self, code):
        """Returns the precondition for implications
        """
        pre = "True"
        expr = getExpression(code)

        if expr == 'implies':
            pre, _ = splitBinary(code) 

        return pre


    def plan(self, code):
        """Returns an optimization dictionary

        's': list of expressions to push down on the left side
        't': list of expressions to push down on the right side
        'st': list of expressions to use for a hash join optimization

        'pre': implication precondition
        """
        return {'s':[], 't':[], 'st':[], 'pre': self.getPrecondition(code)}



