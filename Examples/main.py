from pymc.examples import disaster_model
from pymc import MCMC
from pymc.Matplot import plot
M = MCMC(disaster_model)
M.sample(iter=10000, burn=1000, thin=10)
plot(M)

#hist(M.trace('late_mean')[:])
#show()

