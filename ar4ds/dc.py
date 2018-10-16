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

    def __init__(self, fn, strexp):
        self.fn = fn
        self.strexp = strexp

    def __getitem__(self, dataset):
        
        rules = []
        exceptions = []

        for i in range(len(dataset)):
            s = dataset.iloc[i]
            
            for j in range(len(dataset)):
                t = dataset.iloc[j]

                if self.fn(s,t):
                    rules.append((i,j))
                else:
                    exceptions.append((i,j))

        return ModalConstraint(rules, exceptions)


    def __str__(self):
        return self.strexp



class ModalConstraint(object):

    def __init__(self, rules, exceptions):
        self.rules = rules
        self.exceptions = exceptions

    def __getitem__(self, modal):

        if len(self.rules) == 0:
            return (modal == NEVER)
        
        if len(self.rules) > 0:
            if len(self.exceptions) == 0:
                return (modal == NECESSARY) or \
                       (modal == ALWAYS) or    \
                       (modal == POSSIBLE)

            if len(self.rules) > len(self.exceptions):
                return (modal == USUALLY) or \
                       (modal == POSSIBLE)
            else:
                return (modal == OCCASIONALLY) or \
                        (modal == POSSIBLE)

