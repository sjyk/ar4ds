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

def gt(s,t):
    return (s > t)

def lt(s,t):
    return (s < t)




#logical operators over booleans
def neg(s):
    s,_ = _convert(s,False)
    _check(s)
    return not s

def conj(s,t):
    s,t = _convert(s,t)
    _check(s,t)
    return (s and t)

def disj(s,t):
    s,t = _convert(s,t)
    _check(s,t)
    return (s or t)

def xor(s,t):
    s,t = _convert(s,t)
    _check(s,t)
    return (s and not t) or (not s and t)

def implies(s,t):
    s,t = _convert(s,t)
    _check(s,t)
    return (not s) or t

def iff(s,t):
    s,t = _convert(s,t)
    _check(s,t)
    return implies(s,t) and implies(t,s)


def _convert(s,t):
    try:
        return s.astype('bool'), t.astype('bool')
    except:
        return s,t


# Error checking code
def _check(*args):
    for arg in args:
        if not isinstance(arg, bool):
            AssertionError("The argument " + str(arg) + " is not a boolean")
