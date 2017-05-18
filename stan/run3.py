import pystan as ps
import read
import numpy as np
import argparse
import data
def run(model, use_test_data = False, n_paths = -1):
    continuous = (model == 'model_continuous.stan')
    sfit = ps.stan(file=model,
                   iter = r.iters,
                   chains = r.chains,
                   data=data.get_data(continuous, use_test_data, n_paths))
    print(sfit)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('MODEL')
    parser.add_argument('chains', action='store', type=int)
    parser.add_argument('iters', action='store', type=int)
    parser.add_argument('-t', '--test', help='use small test data', action='store_true')
    parser.add_argument('-p', '--num_pathways', default='-1', help='num_pathways to model. -1 means all', type=int)
    r = parser.parse_args()
    print (r)
    run(r.MODEL, r.test, r.num_pathways)
