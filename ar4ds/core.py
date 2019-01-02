# -*- coding: utf-8 -*-
"""This module contains the basic logical and language primitives
in the ar4ds package. 

The language primitives can be modified to change the naming 
conventions used to define rules and assertions. Our interpreter 
imports the core module so any function placed in here can be used 
in the DSL. By convention, we also try to keep all of the defined 
primitives "pythonic".

Generally, none of the stuff in here should be user facing
"""

import json

#Binary operators over literals

def eq(s,t):
    """Semantically equivalent to python's ==

    You probably don't want to change this too muc as it 
    shows up in a substantial number of the query opt rules.
    """
    return (s == t)

def ne(s,t):
    """Semantically equivalent to python's !="""
    return (s != t)

def gt(s,t):
    """Semantically equivalent to python's >"""
    return (s > t)

def lt(s,t):
    """Semantically equivalent to python's <"""
    return (s < t)

def inr(r,s,t):
    """r is in range of s and t left inclusive"""
    return (r < t) and (r >= s)



"""Logical operators over Booleans

These primitives also run some type checks and format checks. 
There are probably compatibility issues with Python2 to 3 here
Boolean to Int conversion issues are probably all over the place.
"""

def neg(s):
    """Negates a boolean expression."""
    s,_ = _convert(s,False)
    _check(s)
    return not s

def conj(s,t):
    """Logical AND (super important don't rename this)"""
    s,t = _convert(s,t)
    _check(s,t)
    return (s and t)

def disj(s,t):
    """Logical OR (super important don't rename this)"""
    s,t = _convert(s,t)
    _check(s,t)
    return (s or t)

def xor(s,t):
    """Logical XOR kind of useless, but putting it here"""
    s,t = _convert(s,t)
    _check(s,t)
    return (s and not t) or (not s and t)

def implies(s,t):
    """Logical IMPLIES (super important don't rename this)"""
    s,t = _convert(s,t)
    _check(s,t)
    return (not s) or t

def iff(s,t):
    """Logical IFF (super important don't rename this)"""
    s,t = _convert(s,t)
    _check(s,t)
    return implies(s,t) and implies(t,s)



# Error checking code

def _convert(s,t):
    """ This helper routine does a hard type conversion to a boolean.
    """
    try:
        return s.astype('bool'), t.astype('bool')
    except:
        return s,t

def _check(*args):
    for arg in args:
        if not isinstance(arg, bool):
            AssertionError("The argument " + str(arg) + " is not a boolean")

