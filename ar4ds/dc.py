'''
This class defines a denial constraint and 
some basic scaffolding for future inference
'''

NEVER = 'never'
OCCASIONALLY = 'occasionally'
USUALLY = 'usually'
ALWAYS = 'always'
NECESSARY = 'necessary'
POSSIBLE = 'possible'

class DC(object):

    def __init__(self, rule, precond, rexp, precondexp):
        self.rule = rule
        self.precond = precond
        self.rexp = rexp
        self.precondexp = precondexp

    def __getitem__(self, dataset):
        
        rules = set(range(len(dataset)))
        exceptions = set()

        for i in range(len(dataset)):
            s = dataset.iloc[i]
            
            for j in range(len(dataset)):
                t = dataset.iloc[j]

                if not self.precond(s,t) or i == j:
                    
                    if (i in rules):
                        rules.remove(i)
                    
                    if (j in rules):
                        rules.remove(j)

                    continue

                if self.rule(s,t):
                    pass
                else:
                    exceptions.add(i)
                    exceptions.add(j)

        return ModalConstraint(rules.difference(exceptions), exceptions)



    def __str__(self):
        return self.rexp



class ModalConstraint(object):

    def __init__(self, rules, exceptions):
        self.rules = rules
        self.exceptions = exceptions

    def __getitem_frac__(self, t):
        if len(self.rules) == 0 and len(self.exceptions) == 0:
            return False

        else:
            frac = (len(self.rules) + 0.0) /(len(self.rules) + len(self.exceptions))
            return (frac >= t)

    def __getitem__(self, modal):

        try:
            f = float(modal)
            return self.__getitem_frac__(f)
        except:
            pass

        if len(self.rules) == 0 and len(self.exceptions) == 0:
            return (modal == ALWAYS)

        if len(self.rules) == 0:
            return (modal == NEVER)
        
        if len(self.rules) > 0:
            if len(self.exceptions) == 0:
                return (modal == NECESSARY) or \
                       (modal == ALWAYS) or    \
                       (modal == POSSIBLE) or \
                       (modal == USUALLY)

            if len(self.rules) > len(self.exceptions):
                return (modal == USUALLY) or \
                       (modal == POSSIBLE)
            else:
                return (modal == OCCASIONALLY) or \
                        (modal == POSSIBLE)

