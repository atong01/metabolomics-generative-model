"""
Test Run
"""
class Pathway():
    def __init__(self, name, mets):
        self.mets = mets
        self.name = name

def pathways():
    a = Pathway('a', [0])
    b = Pathway('b', [0, 1])
    c = Pathway('c', [2])
    return [a, b, c]

def features():
    return [0, 1, 2]

def detected_features():
    return [True, False, True]

def evidence():
    return [0.99, 0.01, 0.33]

"""
Real Stuff
"""

