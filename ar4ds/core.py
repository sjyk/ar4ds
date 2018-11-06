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


def is_standard_form(dc):
    rule = dc.rexp
    if rule[:7] == "implies":
        cntp = 0
        split_point = 7
        for c in rule[8:]:
            if c == "(" :
                cntp += 1
            elif c == ")":
                cntp -= 1
            if cntp == 0 and c == ",":
                break
            split_point += 1
        a,b = rule[7:split_point], rule[split_point+1:]
        if "disj" in a or "xor" in a or "iff" in a or "implies" in a:
            return False
        cnt = a.count("eq") + a.count("ne") + a.count("ge") + a.count("le")
        if cnt != 1:
            return False
    return True

def hashmap_standard_form(dc, data):
    rule = dc.rexp
    rule = rule.replace(" ", "")
    
    mp = dict()
    header = list(data.columns.values)
    for item in header:
        mp[item] = dict()

    for index, row in data.iterrows():
        for item in header:
            if row[item] not in mp[item]: 
                mp[item][row[item]] = []
            mp[item][row[item]].append(index)
    # print("hash_map:",mp)
    # mp is mapping name of different columns to different sub-hashmaps where values are hashed by their corresponding keys


    if rule[:7] == "implies":
        cntp = 0
        split_point = 7
        for c in rule[8:]:
            if c == "(" :
                cntp += 1
            elif c == ")":
                cntp -= 1
            if cntp == 0 and c == ",":
                break
            split_point += 1
        a = rule[7:split_point+1].split("eq")

    for equality in a[1:]:
        temp = equality[1: -2].split(",")
        compared_col1, compared_col2 = temp[0].split(".")[1], temp[1].split(".")[1]
        # compared_col1 and compared_col2 are the columns needed to compare in each of the equality expressions


        

