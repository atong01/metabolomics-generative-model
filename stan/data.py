import read

def continuous_data(npaths = -1):
    paths, mets, met_mask, y = read.get_matrix_form(True)
    P,M = met_mask.shape
    met_mask = met_mask.T
    if npaths > 0:
        P = npaths
    data_cont = {'P': P,
                'M': M,
                'metabolite_mask': met_mask[:,:P],
                'y': y,
                'detection_shape': 0.01,
                'detection_rate': 0.01,
                'activity_shape': 0.01,
                'activity_rate': 0.01}
    return data_cont

def discrete_data(npaths = -1):
    paths, mets, met_mask, y = read.get_matrix_form(False)
    P,M = met_mask.shape
    if npaths > 0:
        P = npaths

    data = {'P' : P,
            'M' : M,
            'rate_prior' : 1.0,
            'metabolite_mask' : met_mask[:P,:],
            'y' : y,
            'tiny' : 1e-10}
    return data

def continuous_test_data():
    test_data_cont = {  'P': 2,
                        'M': 3,
                        'metabolite_mask': [[0,1],[0,1],[1,0]],
                        'y': [5.1,2.8,1e-9],
                        'detection_shape': 1.0,
                        'detection_rate': 0.01,
                        'activity_shape': 1.0,
                        'activity_rate': 0.01}
    return test_data_cont

def discrete_test_data():
    sample_test_data = { 'P': 2, 
                         'M': 3, 
                         'rate_prior': 1.0, 
                         'metabolite_mask': [[0, 0, 1], 
                                             [1, 1, 0]], 
                         'y': [1, 1, 0],
                         'tiny': 1e-8
                       }
    return sample_test_data

def get_data(is_continuous = True, is_test = False, n_paths = -1):
    if is_continuous:
        if is_test:
            return continuous_test_data()
        return continuous_data(n_paths)
    if is_test:
        return discrete_test_data()
    return discrete_data(n_paths)
