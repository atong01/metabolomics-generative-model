import model
import pymc
import networkx as nx
import matplotlib.pyplot as plt
from pymc import MCMC
from pymc.Matplot import plot
M = MCMC(model)
M.sample(iter=10000, burn=1000, thin=10)
plot(M, path='./plots/test_soft_evidence')

#g = pymc.graph.graph(pymc.Model(model), path='.')
#g.write('model.dot')
#G = nx.drawing.nx_agraph.read_dot('model.dot')
#nx.draw(G)
#plt.draw()

#hist(M.trace('late_mean')[:])
#show()

