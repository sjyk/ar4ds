from .opt import *

class CascadesParseOptState(object):

    def __init__(self, code, s,t, st):
        self.expr = getExpression(code)
        self.arity = getArity(code)
        self.n_arity = len(self.arity)
        self.s = s
        self.t = t
        self.st = st
        self.code = code



class CascadesQueryOptimizer(QueryOptimizer):

    def __init__(self, data):

        self.rules = [ (self._indivisible_expr, self.break_pth),\
                       (self._unitary_expr, self.base_pth),\
                       (self._divisible_expr, self.recurse_pth)]

        super().__init__(data)

    def _unitary_expr(self, state):
        return (state.n_arity == 1)

    def _indivisible_expr(self, state):
        return (state.expr != 'conj' and state.n_arity == 2)

    def _divisible_expr(self, state):
        return (state.expr == 'conj' and state.n_arity == 2)

    def break_pth(self,state):
        state.s.append(None)
        state.t.append(None)
        state.st.append(None)

    def base_pth(self,state):
        if 's' in state.arity:
            state.s.append(state.code)
        else:
            state.t.append(state.code)

    def recurse_pth(self, state):
        b1, b2 = splitBinary(state.code) 
        s1,t1,st1 = self.getPushDownRules(b1)
        s2,t2,st2 = self.getPushDownRules(b2)

        state.s.extend(s1 + s2)
        state.t.extend(t1 + t2)
        state.st.extend(st1 + st2)

    def getPushDownRules(self, code):
        s = []
        t = []
        st = []

        state = CascadesParseOptState(code, s, t, st)

        for rule, opt in self.rules:
            if rule(state):
                opt(state)

        return s,t,st


    def plan(self, code):
        pre = self.getPrecondition(code)
        s,t,st =  [], [], []

        if pre != "True":
            s,t,st = self.getPushDownRules(pre)

        if None in s or None in t or None in st:
            return {'s':[], 't':[], 'st':[], 'pre': pre}
        else:
            return {'s':s, 't':t, 'st':st, 'pre': pre}