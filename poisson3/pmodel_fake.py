from pymc import Gamma, Poisson, InverseGamma
import pymc
import numpy as np
import gen

pathways = gen.pathways()
features = gen.features_dict()
detected = gen.detected_features()
evidence = gen.evidence()
ap =  {p.name : Gamma('p_' + p.name, p.rate, 1) for p in pathways}
#bmp = [Gamma('b_{' + str(i) + '}', 1, ap[i]) for i in range(3)]
bmp = {p.name : {feat : Gamma('b_{' + p.name + ',' + str(feat) + '}', ap[p.name],1) for feat in p.mets} for p in pathways}
print bmp
#g_bmp = {feat : Poisson('g_' + str(feat), sum([bmp[pname][feat] for pname in pathways])) for feat, pathways in features.iteritems()}
g_bmp = {}
for feat, pathways in features.iteritems():
    if detected(feat):
        print feat, "was detected"
        g_bmp[feat] = Poisson('g_' + str(feat), sum([bmp[pname][feat] for pname in pathways]), value = 1, observed = True)
    else:
        print feat, "was not detected"
        g_bmp[feat] = Poisson('g_' + str(feat), sum([bmp[pname][feat] for pname in pathways]))
print g_bmp
