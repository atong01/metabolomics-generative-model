import pystan as ps
import read
import numpy as np
import argparse

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
                    'detection_shape': 0.01,                                      
                    'detection_rate': 0.01,                                       
                    'activity_shape': 0.01,                                       
                    'activity_rate': 0.01} 

#sfit = ps.stan(file='model_continuous.stan', iter = 30000, data=test_data_cont)
sfit = ps.stan(file='model_continuous.stan', 
               iter = r.iters,
               chains = r.chains,
               data=data_cont)
print(sfit)
