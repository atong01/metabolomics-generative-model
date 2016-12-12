import model
import pymc
import networkx as nx
import matplotlib.pyplot as plt
from pymc import MCMC
from pymc.Matplot import plot
M = MCMC(model)
M.sample(iter=500, burn=250, thin=10)
#plot(M, path='./plots')
M.write_csv('out.csv')
#pathways = model.pathways
#traces = {}
#for p in pathways:
#    traces[p] = M.trace(p)[:]
#plt.hist(traces[pathways[0]], bins='auto')
#plt.show()
#t = M.trace(pathways[0])[:]


#g = pymc.graph.graph(pymc.Model(model), path='.')
#g.write('model.dot')
#G = nx.drawing.nx_agraph.read_dot('model.dot')
#nx.draw(G)
#plt.draw()

#hist(M.trace('late_mean')[:])
#show()

