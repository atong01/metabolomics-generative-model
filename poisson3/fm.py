from pymc3 import Bernoulli, Gamma, Poisson, Beta, Model
import pymc3
import numpy as np
import gen
import read
import math

FAKE_DATA = True
epsilon = 1e-10 # prevents log(0)

if FAKE_DATA:
    faker = gen.Test_Generator()
    data = faker.gen('soft1')
else:
    data = read.get_all_sets()


pathways, features, path_dict, reverse_path_dict, evidence, metfrag_evidence = data
for c,v in evidence.items():
    print (c,v )
for c,v in metfrag_evidence.items():
    print (c,v )
print ("num_pathways:", len(pathways))
print ("num_features:", len(features))
print ("num_evidence:", len(evidence))
print ("num_metfrag: ", len(metfrag_evidence))
rate_prior = 0.5
import theano.tensor as T
#eps = Beta('eps', 0.005, 1)
model = Model()
with model:
    eps = 0.0001
    ap =  {p : Gamma('p_' + p, rate_prior, 1) for p in pathways}
    bmp = {p : {feat : Gamma('b_{' + p + ',' + feat + '}', ap[p],1) for feat in path_dict[p]} for p in pathways}
    y_bmp = {}
    g = {}

    def logp_f(f, b, eps):
        if f in evidence:
            return T.log(1 - math.e ** (-1 * b) + epsilon)
        if f in metfrag_evidence:
            a_p = (1.0 / (1 - metfrag_evidence[f])) - 1
            return a_p * T.log(1 - math.e ** (-1 * b) + epsilon) - b
        return T.log(eps) - b
    psi = {}
    for feat, pathways in reverse_path_dict.items():
        y_bmp[feat] = sum([bmp[pname][feat] for pname in pathways])
        g[feat] = Bernoulli('g_' + feat, 1 - math.e ** (-y_bmp[feat]))
        psi[feat] = pymc3.Potential('psi_' + feat, logp_f(feat, y_bmp[feat], eps))
if __name__ == '__main__':
    n=1000
    with model:
        trace = pymc3.sample(n)
        t1 = trace
        print (pymc3.df_summary(trace))
        trace = pymc3.sample(10*n)
        t2 = trace
        print (pymc3.df_summary(trace))
        print (pymc3.stats.compare([t1, t2]))
