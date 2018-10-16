'''
This class defines a denial constraint and 
some basic scaffolding for future inference
'''

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

        return rules, exceptions


    def __str__(self):
        return self.strexp


