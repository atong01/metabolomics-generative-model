from pymc import Bernoulli, Lambda, Beta
import pymc
import numpy as np
import parser
import read

u = [0.01, 0.99]
O = {}
"""
pathways = parser.pathways()
features = parser.features()
detected = parser.detected_features()
evidence = parser.evidence()
"""
data_path = '../data/'
observation_file = data_path + 'HilNeg 0324 -- Data.csv'
cofactors = read.get_cofactors(data_path + 'cofactors')
path_dict = read.get_model(data_path + 'model2.csv', cofactors = cofactors)
pathways = path_dict.keys()
features = read.get_metabolites(path_dict)
evidence = read.metlin(observation_file)
evidence |= read.hmdb(observation_file)
evidence -= cofactors
features -= cofactors
evidence &= features
print evidence
features = list(features)
reverse_path_dict = read.reverse_dict(path_dict)
pi = 0.1

#l = [Beta('lambda_'+p, alpha = 1, beta = 1, value = 0.5) for p in pathways]
l = 0.5
a_ps = [Bernoulli(path, p = l) for i, path in enumerate(pathways)]
#a_ps = [Bernoulli(path, p = l[i]) for i, path in enumerate(pathways)]

for i, p in enumerate(pathways):
    O[p] = {}
    active_path = (lambda x = a_ps[i]: u[1] if x else u[0])
    u_ap = Lambda('u_ap' + str(i), active_path)
    for f in path_dict[p]:
        O[p][f]= (Bernoulli('o_{p=' + p + ',f=' + f + '}', p = u_ap), u_ap)

def is_present(f_id, parents):
    """ Calculates y_f, the probability that a features appears in our sample.
    Args:
        f_id (int): feature id
        O (dict): O is a dict of dicts representing probability of each feature
            in each pathway
    Returns:
        float: y_f
    """
##should probably use log probs
    return 0.99 if any(parents) else 0.01

Y = [Lambda('y_' + str(f), (lambda f_id = f, parents = [O[p][f][0] for p in reverse_path_dict[f]]: is_present(f_id, parents))) for f in features]
Y_os = [Bernoulli('Y_'+features[i], p = y) for i,y in enumerate(Y)]
#Y_os = [Bernoulli('Y_'+str(i), p = y, value = detected[i], observed = True) for i,y in enumerate(Y)]

virtual_prob = [Lambda('v_' + features[i], (lambda y = y: pi if y else 1 - pi)) for i,y in enumerate(Y_os)]
virtual = [Bernoulli('V_'+features[i], p = virtual_prob[i], value = True, observed = True) for i in range(len(Y_os))]
print O['cge00982']['C16591'][0].parents
print Y[0].parents
print Y_os[0].parents
print virtual_prob[0].parents
print virtual[0].parents
