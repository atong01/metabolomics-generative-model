"""
Test Run
"""
class Pathway():
    def __init__(self, name, mets, rate = 1):
        self.mets = mets
        self.name = name
        self.rate = rate

def pathways():
    a = Pathway('a', [0], 1)
    b = Pathway('b', [0, 1], 1)
    c = Pathway('c', [2], 1)
    return [a, b, c]

def features_dict():
    return {0 : ['a', 'b'], 1 : ['b'], 2 : ['c']}

def detected_features():
    f = [True, False, True]
    return lambda x : f[x]

def evidence():
    return [0.99, 0.01, 0.33]

"""
Real Stuff
"""

