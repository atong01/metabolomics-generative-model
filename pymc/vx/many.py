import model
import pymc
from pymc import MCMC
M = MCMC(model)
for i in range(5):
    M.sample(iter=250, burn=50, thin=10)
    M.write_csv('quick/' + str(i) + '.csv')
