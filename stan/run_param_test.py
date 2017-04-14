import pystan as ps
import read
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('chains', action='store', type=int)
parser.add_argument('iters', action='store', type=int)
parser.add_argument('shape', action='store', type=float)
parser.add_argument('rate', action='store', type=float)
r = parser.parse_args()
print ("Parameters Used:")
print (r)

paths, mets, met_mask, y = read.get_matrix_form(True)
P,M = met_mask.shape
met_mask = met_mask.T

data_cont = {'P': P,                                                       
            'M': M,                                                       
            'metabolite_mask': met_mask,                     
            'y': y,                                          
            'detection_shape': r.shape,                                      
            'detection_rate': r.rate,                                       
            'activity_shape': r.shape,
            'activity_rate': r.rate
            }

sfit = ps.stan(file='model_continuous.stan', 
               iter = r.iters,
               chains = r.chains,
               data=data_cont)
print(sfit)
