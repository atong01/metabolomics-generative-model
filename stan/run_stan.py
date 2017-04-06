import pystan as ps
import read

include_soft_evidence = False
paths, mets, met_mask, y = read.get_matrix_form(include_soft_evidence)
P,M = met_mask.shape

sample_test_data = { 'P': 2, 
                     'M': 3, 
                     'rate_prior': 1.0, 
                     'metabolite_mask': [[0, 0, 1], 
                                         [1, 1, 0]], 
                     'y': [1, 1, 0]
                   }

full_test_data  = { 'P' : P,
                    'M' : M,
                    'rate_prior': 1.0,
                    'metabolite_mask' : met_mask,
                    'y' : y
                  }

"""
ps.stan(file='model.stan', 
        data=full_test_data)
"""

test_data_cont = {'P': 2, 
                  'M': 3, 
                  'metabolite_mask': [[0,1],[0,1],[1,0]],
                  'y': [5.1,2.8,1e-9],  
                  'detection_shape': 0.01, 
                  'detection_rate': 0.01, 
                  'activity_shape': 0.01, 
                  'activity_rate': 0.01}
ps.stan(file='model_continuous.stan', 
        data=test_data_cont)
