'''
This module defines the classes that wrap
around boolean rules
'''

#constants
EQ = 0
LT = 1
GT = 2
NE = 3

class HasProperty(object):
    '''
    A property is an equality query of a single 
    tuple.
    '''

    def __init__(self, attribute, value):
        self.attribute = attribute
        self.value = value

    def eval(self, t):
        
        assert(self.attribute in t)

        return (t[self.attribute] == self.value)

    def __str__(self):
        return str(self.attribute) + ' = ' + str(self.value)


class BooleanExpression(object):
    '''
    An expression over a pair of tuples
    '''

    def __init__(self, attribute, op):
        self.attribute = attribute
        self.op = op


    def eval(self, t, s):
        if self.op == EQ:
            return (t[self.attribute] == s[self.attribute])
        elif self.op == GT:
            return (t[self.attribute] > s[self.attribute])
        elif self.op == LT:
            return (t[self.attribute] < s[self.attribute])
        elif self.op == NE:
            return (t[self.attribute] != s[self.attribute])
        else:
            assert(False)

    def __str__(self):
        if self.op == EQ:
            return 'equal on ' + str(self.attribute)
        elif self.op == GT:
            return 'higher on ' + str(self.attribute)
        elif self.op == LT:
            return 'lower on ' + str(self.attribute)
        elif self.op == NE:
            return 'unequal on ' + str(self.attribute)
        else:
            assert(False)



class Expression(object):
    '''
    An expression is a boolean condition on a pair
    of tuples that is implied by the presence 
    of a property.
    '''

    def __init__(self, prop1, prop2, implicant):
        self.prop1 = prop1
        self.p1 = prop1.eval

        self.prop2 = prop2
        self.p2 = prop2.eval

        self.implicant = implicant
        self.i = implicant.eval

    def _implies(self, p, q):
        return (not p) or q

    def eval(self, t, s):
        return self._implies(self.p1(t) and self.p2(s), \
                        self.i(t,s) )

    def evalPrefix1(self,t):
        return (self.p1(t))

    def evalPrefix2(self,t):
        return (self.p2(t))


    def __str__(self):
        return "Left("+str(self.prop1)+ ") and Right("+ str(self.prop2)  + \
               ") => " + str(self.implicant)





class Rule(object):

    def __init__(self, exp, dataset, qp, system=None):
        self.dataset = dataset
        self.qp = qp
        self.exp = exp
        
        self.system = defaultModalSystem

        if system != None:
            self.system = system

        self.refresh()

    def refresh(self):
        self.examples, self.exceptions = \
                self.qp.compute(self.exp, self.dataset)
        self.setModal()


    def setModal(self):
        self.modal = self.system(self.examples, self.exceptions)

    def __str__(self):
        return self.modal+"(" + str(self.exp) + ")"


def size(dictionary):
    count = 0
    for d in dictionary:
        count += len(dictionary[d])
    return count


def defaultModalSystem(examples, exceptions):
    if size(examples) == 0:
        return 'never'
    elif size(self.exceptions) == 0:
        return 'always'
    elif size(self.examples) >= size(self.exceptions):
        return 'usually'
    else:
        return 'occasionally'

def kModalSystem(examples, exceptions):
    if size(examples) == 0:
        return 'impossible'
    elif size(self.exceptions) == 0:
        return 'necessary'
    else:
        return 'possible'
