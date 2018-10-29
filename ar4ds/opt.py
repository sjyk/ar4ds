'''
This module defines the basic primitives for a query optimizer
'''
import ast
import astor

def toAST(code):
    return ast.parse(code)

def toSource(ast):
    return astor.to_source(ast)

