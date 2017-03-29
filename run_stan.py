import pystan as ps

test_data = {'P': 2, 
             'M': 3, 
             'rate_prior': 1.0, 
             'metabolite_mask': [[0, 0, 1], 
                                 [1, 1, 0]], 
             'y': [1, 1, 0]}

ps.stan(file='model.stan', 
        data=test_data)