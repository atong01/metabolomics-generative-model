import pystan
import pickle
from hashlib import md5


def stan_cache(model_code, model_name=None, **kwargs):
    """Use just as you would `stan`"""
    code_hash = md5(model_code.encode('ascii')).hexdigest()
    if model_name is None:
        cache_fn = 'cached-model-{}.pkl'.format(code_hash)
    else:
        cache_fn = 'cached-{}-{}.pkl'.format(model_name, code_hash)
    try:
        sm = pickle.load(open(cache_fn, 'rb'))
    except:
        sm = pystan.StanModel(model_code=model_code)
        with open(cache_fn, 'wb') as f:
            pickle.dump(sm, f)
    else:
        print("Using cached StanModel")
    return sm.sampling(**kwargs)
if __name__ == '__main__':
    model_code = """
        data {
          int<lower=0> N;
          int<lower=0,upper=1> y[N];
        }
        parameters {
          real<lower=0,upper=1> theta;
        }
        model {
          theta ~ beta(0.5, 0.5);  // Jeffreys' prior
          for (n in 1:N)
            y[n] ~ bernoulli(theta);
        }
    """
# with same model_code as before
    data = dict(N=10, y=[0, 1, 0, 0, 0, 0, 0, 0, 0, 1])
    fit = stan_cache(model_code=model_code, data=data)
    print(fit)

    new_data = dict(N=6, y=[0, 0, 0, 0, 0, 1])
# the cached copy of the model will be used
    fit2 = stan_cache(model_code=model_code, data=new_data)
    print(fit2)
