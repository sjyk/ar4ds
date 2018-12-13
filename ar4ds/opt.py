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


def getExpression(code):
    tree = toAST(code)
    try:
        return tree.body[0].value.func.id
    except:
        return None

def getArity(code):
    tree = toAST(code)
    ids = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            if node.id in ('s', 't'): 
                ids.add(node.id)

    return len(ids)

def splitBinary(code):
    atok = asttokens.ASTTokens(code, parse=True)
    calls = []

    for node in ast.walk(atok.tree):
        if isinstance(node, ast.Call):
            calls.append(atok.get_text(node))

    return calls[1], calls[2]

