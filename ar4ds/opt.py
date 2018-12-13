'''
This module defines the basic primitives for a query optimizer
'''
import ast
import astor
import asttokens

def toAST(code):
    return ast.parse(code)

def toSource(ast):
    return astor.to_source(ast)

def isImplicationExpression(code):
    tree = toAST(code)
    return (tree.body[0].value.func.id == "implies")


def splitBinary(code):
    atok = asttokens.ASTTokens(code, parse=True)
    calls = []

    for node in ast.walk(atok.tree):
        if isinstance(node, ast.Call):
            calls.append(atok.get_text(node))

    return calls[1], calls[2]

