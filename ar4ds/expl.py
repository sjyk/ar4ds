from itertools import chain, combinations

def whyeq(data, attr, i, j):
    s = data.iloc[i][attr]
    t = data.iloc[j][attr]
    eq = 'eq'

    attrs = []

    for col in data.columns.values:
        scv = data.iloc[i][col]
        tcv = data.iloc[j][col]

        if col != attr and scv == tcv:
            attrs.append((col, scv, tcv))

    for a in _powerset(attrs):
        if len(a) > 0:
            yield _attr_val_to_rule(_tups_to_conj(a), attr, eq)



def whyie(data, attr, i, j):
    s = data.iloc[i][attr]
    t = data.iloc[j][attr]
    gt = 'gt'

    if t > s:
        gt = 'lt'

    attrs = []

    for col in data.columns.values:
        scv = data.iloc[i][col]
        tcv = data.iloc[j][col]

        if col != attr and scv != tcv:
            attrs.append((col, scv, tcv))

    for a in _powerset(attrs):
        if len(a) > 0:
            yield _attr_val_to_rule(_tups_to_conj(a), attr, gt)


def _powerset(iterable):
    xs = list(iterable)
    # note we return an iterator rather than a list
    return chain.from_iterable(combinations(xs,n) for n in range(len(xs)+1))

def _tups_to_conj(tups):
    rtn = ''
    for tup in tups:
        if rtn == '':
            rtn = _tup_to_conj(tup)
        else:
            rtn = 'conj(' + rtn + "," + _tup_to_conj(tup)+')'

    return rtn

def _tup_to_conj(tup):

    u = tup[1]
    v = tup[2]

    if isinstance(u, str):
        u = '"'+u+'"'

    if isinstance(v, str):
        v = '"'+v+'"'


    s1 = 'eq(s.'+tup[0]+','+str(u)+')'
    t1 = 'eq(t.'+tup[0]+','+str(v)+')'
    return 'conj('+s1+','+t1+')'


def _attr_val_to_rule(conj, implied, op):
    i1 = op + '(s.' + implied + ',t.'+implied+')'
    return 'implies('+conj+','+i1+')', conj


