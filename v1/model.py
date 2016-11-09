from pymc import Bernoulli, Lambda
import pymc
import numpy as np
import parser

u = [0.01, 0.8]
l = 0.5
O = {}
pathways = parser.pathways()
features = parser.features()
detected = parser.detected_features()
evidence = parser.evidence()

a_ps = [Bernoulli('a_'+ str(i), p = l) for i in xrange(len(pathways))]

for i, p in enumerate(pathways):
    O[i] = {}
    active_path = (lambda x = a_ps[i]: u[1] if x else u[0])
    u_ap = Lambda('u_ap' + str(i), active_path)
    for f in p.mets:
        O[i][f]= (Bernoulli('o_{p=' + str(i) + ',f=' + str(f) + '}', p = u_ap), u_ap)

def is_present(f_id, O):
    """ Calculates y_f, the probability that a features appears in our sample.
    Args:
        f_id (int): feature id
        O (dict): O is a dict of dicts representing probability of each feature
            in each pathway
    Returns:
        float: y_f
    """
##should probably use log probs
    tot = 1
    for i, p in O.iteritems():
        for f, o_f in p.iteritems():
            if f_id == f:
                o, u_ap = o_f
                tot = tot * (1 - u_ap)
    return 1 - (tot)

Y = [Lambda('y_' + str(f), (lambda f_id = f, O = O: is_present(f_id, O))) for f in features]
Y_os = [Bernoulli('Y_'+str(i), p = y) for i,y in enumerate(Y)]
#Y_os = [Bernoulli('Y_'+str(i), p = y, value = detected[i], observed = True) for i,y in enumerate(Y)]

virtual_prob = [Lambda('v_' + str(i), (lambda y = y, e = evidence[i]: e if y else 1 - e)) for i,y in enumerate(Y_os)]
for v in virtual_prob:
    print v.value
virtual = [Bernoulli('V_'+str(i), p = virtual_prob[i], value = True, observed = True) for i in range(len(Y_os))]
