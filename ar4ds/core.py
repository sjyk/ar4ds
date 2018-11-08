'''
This module defines the core language
and logic api.
'''
from .dc import *
from .opt import *

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

# Standard form checker
def is_standard_form(dc):
    rule = dc.rexp
    if rule[:7] == "implies":
        cntp = 0 # count of unmatched parentheses
        split_point = 7 # the position of the comma that separates the first half and second half
        for c in rule[8:]:
            if c == "(" :
                cntp += 1
            elif c == ")":
                cntp -= 1
            if cntp == 0 and c == ",":
                break
            split_point += 1
        a,b = rule[7:split_point], rule[split_point+1:] # first and second half
        if "disj" in a or "xor" in a or "iff" in a or "implies" in a or "ne" in a or "ge" in a or "le" in a:
            return False
        cnt = b.count("eq") + b.count("ne") + b.count("ge") + b.count("le")
        if cnt != 1:
            return False
    return True