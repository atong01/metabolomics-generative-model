import pystan as ps
import read
import numpy as np
import argparse

#Test all models

parser = argparse.ArgumentParser()
parser.add_argument('chains', action='store', type=int)
parser.add_argument('iters', action='store', type=int)
r = parser.parse_args()
print (r)

paths, mets, met_mask, y = read.get_matrix_form(True)
P,M = met_mask.shape
met_mask = met_mask.T

data_cont = {'P': P,                                                       
            'M': M,                                                       
            'metabolite_mask': met_mask,                     
            'y': y,                                          
            'detection_shape': 0.01,                                      
            'detection_rate': 0.01,                                       
            'activity_shape': 0.01,                                       
            'activity_rate': 0.01} 
test_data_cont = {  'P': 2,                                                       
                    'M': 3,                                                       
                    'metabolite_mask': [[0,1],[0,1],[1,0]],                       
                    'y': [5.1,2.8,1e-9],                                          
                    'detection_shape': 1.0,                                      
                    'detection_rate': 0.01,                                       
                    'activity_shape': 1.0,                                       
                    'activity_rate': 0.01} 
sample_test_data = { 'P': 2, 
                     'M': 3, 
                     'rate_prior': 1.0, 
                     'metabolite_mask': [[0, 0, 1], 
                                         [1, 1, 0]], 
                     'y': [1, 1, 0],
                     'tiny': 1e-8
                   }
def test_all():
    sfit = ps.stan(file='model.stan', 
                   iter = r.iters,
                   chains = r.chains,
                   data=sample_test_data)
    print(sfit)

    sfit = ps.stan(file='model_simple.stan', 
                   iter = r.iters,
                   chains = r.chains,
                   data=sample_test_data)
    print(sfit)

    sfit = ps.stan(file='model_continuous.stan', 
                   iter = r.iters,
                   chains = r.chains,
                   data=test_data_cont)
    print(sfit)
def test_continuous():
    sfit = ps.stan(file='model_continuous.stan', 
                   iter = r.iters,
                   chains = r.chains,
                   data=test_data_cont)
    print(sfit)
    sfit = ps.stan(file='model_continuous.stan', 
                   iter = 10*r.iters,
                   chains = r.chains,
                   data=test_data_cont)
    print(sfit)

if __name__ == '__main__':
    test_continuous()
