import read


def ab_test():
    """ One on pathway vs one off pathway. 
    """
    pathways    = ['a', 'b']
    features    = ['1', '2']
    path_dict   = {'a' : ['1'], 'b' : ['2']}
    evidence    = set(['1'])
    return pathways, features, path_dict, evidence, None

def abc_test():
    """ Expected A > C > B """
    pathways = ['a', 'b', 'c']
    features = ['1', '2', '3']
    path_dict = {'a':['1', '2'], 'b':['2'], 'c': ['3']}
    evidence = set(['1', '2'])
    return pathways, features, path_dict, evidence, None

def abc2_test():
    """ Expected C > A > B """
    pathways = ['a', 'b', 'c']
    features = ['1', '2', '3']
    path_dict = {'a':['1', '2'], 'b':['2'], 'c': ['3']}
    evidence = set(['1', '3'])
    return pathways, features, path_dict, evidence, None
    
def abc3_test():
    """ Expected C > B > A """
    pathways = ['a', 'b', 'c']
    features = ['1', '2', '3']
    path_dict = {'a':['1', '2'], 'b':['2'], 'c': ['3']}
    evidence = set(['2', '3'])
    return pathways, features, path_dict, evidence, None

def soft_single_node_test():
    pathways = ['a']
    features = ['1']
    path_dict = {'a' : ['1']}
    soft_evidence = {'1' : 0.5}
    return pathways, features, path_dict, set(), soft_evidence

def soft_compare_regular_evidence_test():
    """ Expected A > B > C """
    pathways = ['a', 'b', 'c']
    features = ['1', '2', '3']
    path_dict = {'a':['1'], 'b':['2'], 'c': ['3']}
    evidence = set(['1'])
    soft_evidence = {'2' : 0.5}
    return pathways, features, path_dict, evidence, soft_evidence

class Test_Generator():
    def __init__(self):
        self.tests = {
                        'ab'    : ab_test,
                        'abc'   : abc_test,
                        'abc2'  : abc2_test,
                        'abc3'  : abc3_test,
                        'soft0' : soft_single_node_test,
                        'soft1' : soft_compare_regular_evidence_test,
                     }

    def gen(self, test_name):
         pathways, features, path_dict, evidence, met_evidence = self.tests[test_name]()
         rev_path_dict = read.reverse_dict(path_dict)
         evidence = {e : 1 for e in evidence}
         if met_evidence is None: 
             met_evidence = dict()
         return pathways, features, path_dict, rev_path_dict, evidence, met_evidence

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
