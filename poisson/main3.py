import model3
import pymc
#import networkx as nx
import matplotlib.pyplot as plt
from pymc import MCMC
from pymc.Matplot import plot
M = MCMC(model3)
#MAP = pymc.MAP(model3)
#MAP.fit()
def get_coeffs(map_):
    return [{str(v) : v.value} for v in map_.variables if str(v).startswith('p') or str(v).startswith('b') or str(v).startswith('e')]

#print get_coeffs(MAP)
M.sample(iter=10000, burn=250, thin=10)
#plot(M, path='./plots')
M.write_csv('out.csv')
#pathways = model.pathways
#traces = {}
#for p in pathways:
#    traces[p] = M.trace(p)[:]
#plt.hist(traces[pathways[0]], bins='auto')
#plt.show()
#t = M.trace(pathways[0])[:]


#import networkx as nx
g = pymc.graph.graph(pymc.Model(model3), path='.')
g.write_png('model.png')
#G = nx.drawing.nx_agraph.read_dot('model.dot')
#nx.draw(G)
#plt.show()

#hist(M.trace('late_mean')[:])
#show()

