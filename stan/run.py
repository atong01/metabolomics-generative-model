import pystan as ps
import read
import numpy as np
import argparse
import data
def run(continuous = True, use_test_data = False):
    f = 'model_continuous.stan' if continuous else 'model_simple.stan'
    sfit = ps.stan(file=f,
                   iter = r.iters,
                   chains = r.chains,
                   data=data.get_data(continuous, use_test_data))
    print(sfit)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('chains', action='store', type=int)
    parser.add_argument('iters', action='store', type=int)
    parser.add_argument('-d', '--use_discrete_data', action='store_true')
    parser.add_argument('-t', '--test', help='use small test data', action='store_true')
    r = parser.parse_args()
    print (r)
    run(not r.use_discrete_data, r.test)
