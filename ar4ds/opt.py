'''
This module defines the basic primitives for a query optimizer
'''
import ast

def toAST(code):
    return ast.parse(code)

def toSource(ast):
    return astor.to_source(ast)

