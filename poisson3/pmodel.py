from pymc import Bernoulli, Gamma, Poisson, InverseGamma
import pymc
import numpy as np
import gen
import read
import math

ONE, ZERO = (0.99, 0.01)

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
reverse_path_dict = read.reverse_dict(path_dict)
metfrag = read.metfrag(observation_file)
metfrag_evidence = read.dict_of_set(read.metfrag_with_scores(observation_file, keep_zero_scores = False), metfrag & features - cofactors - evidence)
evidence = {e : 1 for e in evidence}

rate_prior = 0.5

ap =  {p : Gamma('p_' + p, rate_prior, 1) for p in pathways}
bmp = {p : {feat : Gamma('b_{' + p + ',' + feat + '}', ap[p],1) for feat in path_dict[p]} for p in pathways}
y_bmp = {}
virtual = {}

se_count = 0
for feat, pathways in reverse_path_dict.iteritems():
    #g_bmp[feat] = Poisson('g_' + feat, sum([bmp[pname][feat] for pname in pathways]))
    y_bmp[feat] = Bernoulli('y_' + feat, 1 - math.e ** -sum([bmp[pname][feat] for pname in pathways]))
#    if feat in evidence:
#        virtual[feat] = Bernoulli('ve_' + feat, ONE if (g_bmp[feat] != 0) else ZERO, value = 1, observed = True)
#    elif feat in metfrag_evidence:
#        se_count += 1
#        e = metfrag_evidence[feat]
#        virtual[feat] = Bernoulli('vs_' + feat, e if (g_bmp[feat] != 0) else 1 - e, value = 1, observed = True)

