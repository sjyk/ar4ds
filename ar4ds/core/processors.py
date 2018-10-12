
class Naive(object):

    def __init__(self):
        self.name = "naive"

    def compute(self, exp, dataset):
        examples = {}
        exceptions = {}

        for i in range(0, len(dataset)):

            s = dataset.loc[i]

            if not exp.evalPrefix1(s):
                continue

            if i not in exceptions:
                exceptions[i] = []

            if i not in examples:
                examples[i] = []

            for j in range(0, len(dataset)):
                t = dataset.loc[j]

                if not exp.evalPrefix2(t):
                    continue

                if i == j:
                    continue

                if exp.eval(s,t):
                    examples[i].append(j)
                else:
                    exceptions[i].append(j)

        return examples, exceptions




