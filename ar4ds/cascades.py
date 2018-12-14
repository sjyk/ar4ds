from .opt import *


class CascadesQueryOptimizer(QueryOptimizer):

    def __init__(self, data):
        super().__init__(data)


    def getPushDownRules(self, code):
        s = []
        t = []
        st = []

        expr = getExpression(code)
        arity = getArity(code)
        larity = len(arity)

        if expr != 'conj' and larity == 2:
           s.append(None)
           t.append(None)
           st.append(None)

        elif expr == 'conj' and larity == 2:
           b1, b2 = splitBinary(code) 
           s1,t1,st1 = self.getPushDownRules(b1)
           s2,t2,st2 = self.getPushDownRules(b2)

           s += s1 + s2
           t += t1 + t2
           st += st1 + st2

        elif larity == 1:
            if 's' in arity:
                s.append(code)
            else:
                t.append(code)

        else:
           s.append(None)
           t.append(None)
           st.append(None)

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