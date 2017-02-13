from pymc import Gamma, Poisson, InverseGamma
import pymc
import numpy as np
import gen
import read

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
rate_prior = 0.5
print evidence

ap =  {p : Gamma('p_' + p, rate_prior, 1) for p in pathways}
bmp = {p : {feat : Gamma('b_{' + p + ',' + feat + '}', ap[p],1) for feat in path_dict[p]} for p in pathways}
g_bmp = {}
for feat, pathways in reverse_path_dict.iteritems():
    if feat in evidence:
        g_bmp[feat] = Poisson('g_' + feat, sum([bmp[pname][feat] for pname in pathways]), value = 1, observed = True)
    else:
        g_bmp[feat] = Poisson('g_' + feat, sum([bmp[pname][feat] for pname in pathways]))
