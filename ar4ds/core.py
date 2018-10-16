'''
This module defines the core language
and logic api.
'''
from .dc import *

def compile(rule="True", pre="True"):
    return DC(eval('lambda s,t: ' + rule), \
              eval('lambda s,t: ' + pre), \
              rule, pre)


#binary operators over literals
def eq(s,t):
    return (s == t)

def ne(s,t):
    return (s != t)

def ge(s,t):
    return (s > t)

def le(s,t):
    return (s < t)




#logical operators over booleans
def neg(s):
    _check(s)
    return not s

def conj(s,t):
    _check(s,t)
    return (s and t)

def disj(s,t):
    _check(s,t)
    return (s or t)

def xor(s,t):
    _check(s,t)
    return (s and not t) or (not s and t)

def implies(s,t):
    _check(s,t)
    return (not s) or t

def iff(s,t):
    _check(s,t)
    return implies(s,t) and implies(t,s)




# Error checking code
def _check(*args):
    for arg in args:
        if not isinstance(arg, bool):
            AssertionError("The argument " + arg + " is not a boolean")
